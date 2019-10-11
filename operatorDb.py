import pymysql
#操作数据库获取桩号端口号
def QueryStakePort(cf):
    stake_port = []
    STAKEID = []
    host = cf.get("DB", "Host")  # 数据库IP
    port = int(cf.get("DB", "Port"))  # 数据库端口号
    user = cf.get("DB", "User") # 用户名
    password = cf.get("DB", "Password")  # 密码
    db = cf.get("DB", "Db") # DB
    stationId = cf.get("STATION", "ID") #站号
    stationNum = "424090000"
    if (len(stationId) == 1): #拼接字符串 当站号位数不够时用0补齐
        station = stationNum + "0" + stationId
    else:
        station = stationNum + stationId

    print("StationId:",station)

    # 打开数据库连接
    db = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select ass.STAKE_NO ,po.chargeNo from (SELECT ASP.CHARGER_NO as chargeNo, ASP.STAKE_UUID as stake_uuid FROM ASSET_PORT ASP LEFT JOIN ASSET_STATION AST ON AST.UUID = ASP.STATION_UUID WHERE AST.STATION_NO = "+ station + ") as po left join asset_stake as ass on po.stake_uuid = ass.uuid order by STAKE_NO"
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            id = row[0]
            name = row[1]
            stake_port.append([row[0], row[1]])
            #STAKEID.append(row[0])
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    print ("STAKE:PORT-->",stake_port)
    return stake_port