from db import connect_online
import pandas as pd

def purification(p):
    conn = connect_online()

    command = [f"operating_system = '{p['os']}'",
               f"screen_size between {p['ss_min']} and {p['ss_max']}",
               f"internal_memory between {p['s_min']} and {p['s_max']}",
               f"price between {p['p_min']} and {p['p_max']}"]
    
    sand ='and'
    if p['os'] == 'Any':
        command[0] = ''
    if p['ss_min'] == 'Any':
        command[1] = ''
    if p['s_min'] == 'Any':
        command[2] = ''
    if p['p_min'] == 'Any':
        command[3] = ''

    if p['use_case'] == 'Any':
        if command.count('') == 4:
            query = """select brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price from phonestable"""
        else:
            query = f"""select brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price from phonestable where """
            c = 0
            for i in command:
                if i != '':
                    if c == 0:
                        query += f"{i} "
                        c+=1
                    else:
                        query += f"{sand} {i} "
                
    else:
        
        if p['use_case'] == 'Gaming':
            query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE (RAM >= 8 AND internal_memory >= 128) AND screen_size >= 6.0 AND battery_size >= 4000"""
        elif p['use_case'] == 'Photography':
            query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE main_camera >= 48 AND selfie_camera >= 12"""
        elif p['use_case'] == 'Large Screen':
            query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE screen_size >= 6.0"""
        elif p['use_case'] == 'Great Battery Life':
            query = """SELECT brand || ' ' || model AS "Phone", internal_memory, ram, battery_size, screen_size, price FROM phonestable WHERE battery_size >= 4500"""

        if p['os'] != 'Any':
            query += " AND operating_system = '{}'".format(p['os'])

        query += " ORDER BY"
        if p['use_case'] == 'Gaming':
            query += " performance DESC"
        elif p['use_case'] == 'Photography':
            query += " main_camera DESC, selfie_camera DESC"
        elif p['use_case'] == 'Large Screen':
            query += " screen_size DESC"
        elif p['use_case'] == 'Great Battery Life':
            query += " battery_size DESC"
            
    if conn:
        df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df
