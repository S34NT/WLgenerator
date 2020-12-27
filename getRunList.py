from pyppeteer.launcher import launch
import asyncio
import mysql.connector
import webbrowser
import sys



async def fetchList(listName):

    #async def downloadRunList():
        #click on the see all vehicles button
        #event_list > div > div > div > div.left > div.buttons > a:nth-child(1)


    async def checkForListName(linkTexts, listName):
        
        isFound = False
        #for each link that was pulled, check if the name matches the requested list name
        for element in linkTexts:
            oneAuction = await page.evaluate('(element) => element.textContent',element)
            print(oneAuction)
            
            #if the list is found, click the link
            if(listName in oneAuction):
                await page.evaluate('(element) => element.click()',element)
                await page.waitForSelector('#event_list > div > div > div > div.left > div.buttons > a:nth-child(1)')
                await page.click('#event_list > div > div > div > div.left > div.buttons > a:nth-child(1)')
                await page.waitFor(3000)
                #set the download location for the runlist .csv file
                cdp = await page.target.createCDPSession()
                await cdp.send('Page.setDownloadBehavior', { 'behavior': 'allow', 'downloadPath': 'C:\\Users\\Sean\\Desktop\\Dealership'})

                #click the download link which will download the runlist as .csv file
                
                await page.waitForSelector('#content_for_layout > ul > li:nth-child(4) > a')
                await page.click('#content_for_layout > ul > li:nth-child(4) > a')
                await page.waitFor(5000)
                
                isFound = True
                return(isFound)

        return(isFound)


    browser = await launch({"headless": False})
    page = await browser.newPage()
    await page.goto('https://www.edgepipeline.com/dashboard')

    #wait for the login page to load, then enter the required info to login
    await page.waitForSelector('#username')
    await page.click('#username')
    await page.keyboard.type('s34nt')

    await page.waitForSelector('#password')
    await page.click('#password')
    await page.keyboard.type('xr6421x')

    await page.click('#login_box > form > div.submit_buttons > input')
   
    
    try:
        
    
        #check if there are runlists for today
        try:
            await page.waitForSelector('#dashboard-calendar > div.calendar > ul > li:nth-child(3) > ul > li > a', timeout = 2000 )
        except:

            pass
        
        #check if there are runlists for tomorrow
        try:
            await page.waitForSelector('#dashboard-calendar > div.calendar > ul > li:nth-child(4) > ul > li > a', timeout = 2000)
        except:
            pass
        
      
        linkTextsToday = await page.querySelectorAll('#dashboard-calendar > div.calendar > ul > li:nth-child(2) > ul > li>  a')
        linkTextsTomorrow = await page.querySelectorAll('#dashboard-calendar > div.calendar > ul > li:nth-child(3) > ul > li > a')
     
        found = await checkForListName(linkTextsToday, listName)
        if(found == False):
            found = await checkForListName(linkTextsTomorrow, listName)

        #if the specified runlist is found, download it to the current directory
        if(found == True):
            #download the runlist
            #await downloadRunList()
            print("runlist found")
        else:
            print("runlist was not found")
            exit(0)

    except Exception as e:
        print("no runlist was found")
        print(e)
        exit(0)
        
 
#close the browser after getting the runlist  
    await page.waitFor(1500)
    await browser.close()

