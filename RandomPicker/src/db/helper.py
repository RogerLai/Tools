import torndb
import tornado
import oursql
from common.config import DB_SREVER, DB_USER, DB_PASSWORD, DB_SCHEMA, DBPOOL
from common.exceptions import SQLError
from common import utils

def select(sql_stmt, params):
    try:
        conn = torndb.Connection(DB_SREVER, DB_SCHEMA, user = DB_USER, password = DB_PASSWORD)
        if params:
            result = conn.query(sql_stmt, params)
        else:
            result = conn.query(sql_stmt)
            
    except Exception,e:
        tornado.log.logging.error(e)
        raise SQLError
    else:
        return result
    finally:
        if 'conn' in locals():
            conn.close()

def update(sql_stmt, params):
    try:
        conn = torndb.Connection(DB_SREVER, DB_SCHEMA, user = DB_USER, password = DB_PASSWORD)
        result = conn.execute_rowcount(sql_stmt, params)
    except Exception,e:
        tornado.log.logging.error(e)
        raise SQLError
    else:
        return result
    finally:
        if 'conn' in locals():
            conn.close()
            
def insert(sql_stmt, params):
    try:
        conn = torndb.Connection(DB_SREVER, DB_SCHEMA, user = DB_USER, password = DB_PASSWORD)
        result = conn.execute_lastrowid(sql_stmt, params)
    except Exception,e:
        tornado.log.logging.error(e)
        raise SQLError
    else:
        return result
    finally:
        if 'conn' in locals():
            conn.close()            


def get_record_fromdb(record_id, tab):
    if record_id is None:
        return None
    
    if (tab not in ['alipay_payment_tracking']):
        record_id = long(record_id)
    
    sql_strs = {'user': 'SELECT user_id, name, gender, age, email, mobile, icon_url, preview_icon_url, web_preview_icon_url, is_valid, is_admin, is_poster, post_count FROM user WHERE user_id = ?',
                } 
    
    keys = {'user': 'user_id'}
    
    try:
        # get connection from connection pool
        conn = DBPOOL.connection()
        cursor = conn.cursor(oursql.DictCursor)

        rec = {}
        
        cursor.execute(sql_strs[tab], (record_id,))
        for row in cursor:
            rec = row
            
        if rec:
            rec[keys[tab]] = record_id
        
    except Exception,e:
        tornado.log.logging.error(e)
        raise SQLError
    else:        
        return rec
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    

def get_bundle_fromdb(res_list, tab, *dyn_params):
    res_list = res_list[:]
    sql_strs = {'user': 'SELECT user_id, name, gender, age, mobile, icon_url, preview_icon_url, web_preview_icon_url, is_service_provider, last_latitude, last_longitude FROM user WHERE user_id in (%s)',
                }
    
    keys = {'user': 'user_id'}
    
    # concat the in clause
    in_clause = utils.in_clause(res_list)
        
    if in_clause == '':
        return res_list
    else:    

        try:
            # get connection from connection pool
            conn = DBPOOL.connection()
            cursor = conn.cursor(oursql.DictCursor)
            
            if dyn_params:
                cursor.execute(sql_strs[tab] % in_clause, dyn_params)
            else:
                cursor.execute(sql_strs[tab] % in_clause)
                
            result_set = cursor.fetchall()
            
            rec_set = {}
            for row in result_set:
                # put into result set
                rec_set[row[keys[tab]]] = row
                
            # update the return list
            for i in xrange(len(res_list)):
                if type(res_list[i]) in (int, long):
                    res_list[i] = rec_set.get(res_list[i])
            
        except Exception,e:
            tornado.log.logging.error(e)
            raise SQLError
        else:
            return res_list
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close() 

# for update query sqls            
def insert_or_update_query(sql_statment, sql_params, conn_close_flag = True):
    try:
        conn = DBPOOL.connection()            
        cursor = conn.cursor()        
        cursor.execute(sql_statment, sql_params)        
        conn.commit()
        return True
    except Exception, e:
        tornado.log.logging.error(e)
        raise SQLError
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None and conn_close_flag == True):
            conn.close()

# for select query sqls            
def select_query(sql_statment, sql_params = None, dict_flag = False, sql_key = None, conn_close_flag = True):
    #server_log.debug("try to execute query %s with parameters %s " % (sql_statment, sql_params))
    try:
        conn = DBPOOL.connection()
        
        if (dict_flag == True):                
            cursor = conn.cursor(oursql.DictCursor)            
        else:
            cursor = conn.cursor()
        
        if (sql_params is not None):
            cursor.execute(sql_statment, sql_params)
        else:
            cursor.execute(sql_statment)
            
        if (sql_key is not None):
            result = {}            
            for row in cursor:
                result[row[sql_key]] = row
        else:
            result = cursor.fetchall()
                           
        return result
    
    except Exception, e:
        tornado.log.logging.error(e)
        raise SQLError
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None and conn_close_flag == True):
            conn.close()