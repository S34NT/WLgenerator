
import pandas as pd  
import glob as gb
import asyncio
from pyppeteer.launcher import launch
from carRanking import rankCars
from styleMatcher import similar
from tabulate import tabulate
import webbrowser





#Launch headless chrome with pyppeteer
async def main():
    browser = await launch({"headless": False})
    page = await browser.newPage()
    await page.goto('https://mmr.manheim.com/?country=US&popup=true&source=man', timeout = 40000)
   
    #Wait for redirection to login page    
    await page.waitForSelector('#user_username', timeout = 30000)

    #Login with username and password
    user_name = "noahscheidmantel"
    password = "Noahs6427!"

    await page.click('#user_username')
    await page.keyboard.type(user_name)
    await page.click('#user_password')
    await page.keyboard.type(password)
    await page.click('#submit')

    for file in gb.glob("./*.csv"):
                                            #Target columns
        df = pd.read_csv(file, usecols = list(range(0,15)), sep = ',')
    
        #convert df to dataframe format
        df = pd.DataFrame(df)

        #print the filename 
        print(file)

        #initialize lists for the new columns to be appended to the original table
        adjustedMMR = []
        baseMMR = []
        lowRange = []
        highRange = []
        avgOdom = []
        avgCond = []

    #Counter for looping through table
    row_count = df.shape[0]

    for x in range(row_count):

        vin = (df.iloc[x, 14])
        grade = (df.iloc[x, 9])
        grade = str(grade).replace('.','')
        grade = grade.lstrip('0')
        color = (df.iloc[x, 7])
        color = str(color).title()
        odometer = (df.iloc[x, 6])
        odometer = str(odometer)
        style = (df.iloc[x, 5])
        style = str(style)

        print(vin)
        #styleType = checkStyleType(style)
        #print(styleType) #(FOR TESTING)


        
        #clear the contents in the vin input box
        await page.waitForSelector('#vinText', timeout = 5000) 
        clearVin = await page.querySelector('#vinText')
        await page.evaluate('(clearVin) => clearVin.value = ""', clearVin)
    
        
        await page.click('#vinText')
        await page.keyboard.type(vin)
        await page.waitForSelector('.styles__vinButton__3v5fK', timeout = 5000)
        await page.click('.styles__vinButton__3v5fK')
        await page.waitFor(1000)

        try:
            errCheck = await page.querySelector('.styles__vinErrorMsg__BgmAu')
            errMsg = await page.evaluate('(errCheck) => errCheck.textContent', errCheck)
            if(errMsg != ''):
                baseMMR.append("0")
                adjustedMMR.append("0")
                avgOdom.append("0")
                avgCond.append("0")
                lowRange.append("0")
                highRange.append("0")
                continue

        except Exception as e:
            print(e)
            pass

        try:
            #Check for the popup window, if one exists grab the selectors 
            #from the table where style types are entered
            await page.waitForSelector('.styles__modalContainer__2phk2', timeout = 5000)
            trs = await page.querySelectorAll('td:nth-child(4)')
            
            #Check style type attribute against the known style types
            #Then select appropraite style type from popup window
            similarity = 0
            targetElement = trs[0]
            for element in trs:
                data = await page.evaluate('(element) => element.textContent',element)

                tmpSim = similar(data, style)
                
                if(tmpSim > similarity):

                    similarity = tmpSim
                   
                    targetElement = element

            await page.evaluate('(targetElement) => targetElement.click()', targetElement)

                                      
        except Exception as e:
            #print(e) 
            pass
            #do nothing


        try:
            #clear out the MMR data from previous car
            await page.waitForSelector('.styles__clearAdjustment__2rWoh', timeout = 5000)
            await page.click('.styles__clearAdjustment__2rWoh')

            await page.waitForSelector('#Odometer', timeout = 10000)



            #Fill out the MMR adjustments

            #await page.waitForSelector('#Odometer', timeout = 4000)
            await page.click('#Odometer')  
            await page.waitFor(600)
            await page.type('#Odometer', odometer)
            await page.waitFor(600)
            await page.waitForSelector('.icon-checkmark-bold', timeout = 5000)
            await page.click('.icon-checkmark-bold')

            await page.waitForSelector('#Grade', timeout = 5000)
            await page.select('#Grade', grade)

            await page.waitForSelector('.styles__button__rqYJE', timeout = 3000)
            await page.click('.styles__button__rqYJE')

            await page.waitForSelector('#Ext\ Color', timeout = 3000)
            await page.select('#Ext\ Color', str(color))
            
            await page.waitForSelector('#Region', timeout = 3000)
            await page.select('#Region', "MW")
            await page.waitFor(1000)

            #get the Base MMR from the web page
            await page.waitForSelector('.styles__currencyContainer__2XYTl > div:nth-child(1)', timeout = 3000)
            element1 = await page.querySelector('.styles__currencyContainer__2XYTl > div:nth-child(1)')

            #TODO: exclude cars with bMMR > 10,000

            baseMMR.append(await page.evaluate('(element1) => element1.textContent', element1))

            #get the average number of miles on Odometer
            await page.waitForSelector('.styles__odometer__B09kL > div:nth-child(1) > div:nth-child(2)', timeout = 3000)
            element2 = await page.querySelector('.styles__odometer__B09kL > div:nth-child(1) > div:nth-child(2)')
            avgOdom.append(await page.evaluate('(element2) => element2.textContent', element2))

            #get the average condition
            await page.waitForSelector('.styles__condition__mT-JJ > div:nth-child(1) > div:nth-child(2)', timeout = 3000)
            element3 = await page.querySelector('.styles__condition__mT-JJ > div:nth-child(1) > div:nth-child(2)')
            avgCond.append(await page.evaluate('(element3) => element3.textContent', element3))

            #get the typical lower end range
            await page.waitForSelector('.styles__valueSpread__3U9KX > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)', timeout = 3000)
            element4 = await page.querySelector('.styles__valueSpread__3U9KX > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
            lowRange.append(await page.evaluate('(element4) => element4.textContent', element4))

            #get the typical higher end range
            await page.waitForSelector('.styles__valueSpread__3U9KX > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)', timeout = 3000)
            element5 = await page.querySelector('.styles__valueSpread__3U9KX > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)')
            highRange.append(await page.evaluate('(element5) => element5.textContent', element5))

            #get adjusted MMR
            await page.waitForSelector('div.undefined > div:nth-child(1)', timeout = 3000)
            element6 = await page.querySelector('div.undefined > div:nth-child(1)')
            adjustedMMR.append(await page.evaluate('(element6) => element6.textContent', element6))

            #Clear the MMR adjustments by clicking the 'clear' button
            await page.waitForSelector('.styles__clearAdjustment__2rWoh', timeout = 2000)
            await page.click('.styles__clearAdjustment__2rWoh')


            print("baseMMR: %s\nadjustedMMR: %s\nlowRange: %s\nhighRange: %s\n " %(baseMMR[x], adjustedMMR[x], lowRange[x], highRange[x]))
        
        except Exception as e:
            print(e)
            print("Not enough transaction data available to generate MMR\n")
            baseMMR.append("0")
            adjustedMMR.append("0")
            avgOdom.append("0")
            avgCond.append("0")
            lowRange.append("0")
            highRange.append("0")

    await page.waitFor(3000)
    
    await browser.close()

    df['baseMMR'] = pd.Series(list(baseMMR))
    df['adjustedMMR'] = pd.Series(list(adjustedMMR))
    df['lowRange'] = pd.Series(list(lowRange))
    df['highRange'] = pd.Series(list(highRange))
    df['avgOdom'] = pd.Series(list(avgOdom))
    df['avgCond'] = pd.Series(list(avgCond))
    rankings = rankCars(df)
    df['rank'] = pd.Series(list(rankings))

    df.drop(df.index[df['rank'] == 0.0], inplace = True)

    df = df.sort_values(by = 'rank', ascending = False)

    df.to_csv('newRunList.csv')
    pdtabulate=lambda df:tabulate(df, headers='keys', tablefmt='html')
    

    f = open("output.html", "x")
    f.write(pdtabulate(df))
    f.close()


    webbrowser.open_new_tab('./output.html')
   
   
asyncio.get_event_loop().run_until_complete(main())




    
