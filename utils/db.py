import aiosqlite

#===============================================================================

async def create_db():
    async with aiosqlite.connect("economy.db") as db:
        cursor = await db.cursor()
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS eco (
            memberid INTEGER,
            money INTEGER 
        )
        """)
        query = '''
        CREATE TABLE IF NOT EXISTS marketrole (
            memberid INTEGER,
            roleid INTEGER,
            cashselling INTEGER
        )
        '''
        await cursor.execute(query)
        await db.commit()

#===============================================================================

async def adddb(member):
    async with aiosqlite.connect("economy.db") as db:
        await db.execute("INSERT INTO eco (memberid, money) VALUES (?, ?)", (member, 0))
        await db.commit()

async def removedb(member):
    async with aiosqlite.connect("economy.db") as db:
        await db.execute("DELETE FROM eco WHERE memberid=?", (member))
        await db.commit()

async def addmoneydb(member, t):
    async with aiosqlite.connect('economy.db') as db:
        await db.execute("UPDATE eco SET money = money + ? WHERE memberid = ?", (t, member))
        await db.commit()
        
async def removemoneydb(member, t):
    async with aiosqlite.connect('economy.db') as db:
        await db.execute("UPDATE eco SET money = money - ? WHERE memberid = ?", (t, member))
        await db.commit()

async def getbalancedb(member):
    async with aiosqlite.connect('economy.db') as db:
        cursor = await db.execute("SELECT money FROM eco WHERE memberid=?", (member,))
        b = await cursor.fetchone()
        return b[0]
    
#===============================================================================

async def addroledb(member, t):
    async with aiosqlite.connect("economy.db") as db:
        await db.execute("INSERT INTO marketrole (memberid, roleid, cashselling) VALUES (?, ?, ?)", (member, t, 100))
        await db.commit()

async def fetch_market_role():
    async with aiosqlite.connect('economy.db') as db:
        cursor = await db.execute("SELECT memberid, roleid, cashselling FROM marketrole")
        b = await cursor.fetchall()
        return b
    
async def buy_market_role(member):
    b = await getbalancedb(member)
    async with aiosqlite.connect('economy.db') as db:
        cursor = await db.execute("SELECT memberid, roleid, cashselling FROM marketrole")
        b = await cursor.fetchall()
        return b

#===============================================================================