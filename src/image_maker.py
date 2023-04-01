from PIL import Image, ImageDraw, ImageFont
import pandas as pd

class ImageMaker:
    
    def __init__(__self__):
        
        __self__.montserrat_giant = ImageFont.truetype("./assets/fonts/Montserrat-Regular.otf", 70)
        __self__.montserrat_extrabold = ImageFont.truetype("./assets/fonts/Montserrat-ExtraBold.otf", 70)
        __self__.montserrat_small = ImageFont.truetype("./assets/fonts/Montserrat-Regular.otf", 60)
        
        __self__.image = Image.open('./assets/template/image.png')
        __self__.image2 = Image.open('./assets/template/image2.png')
        __self__.image3 = Image.open('./assets/template/image3.png')
        
        __self__.arrow_green = Image.open('./assets/template/green_arrow.png')
        __self__.arrow_red = Image.open('./assets/template/red_arrow.png')
        __self__.nothing = Image.open('./assets/template/nothing.png')
        __self__.white_bar = Image.open('./assets/template/white_bar.png')
        
        __self__.draw = ImageDraw.Draw(__self__.image)
        __self__.draw2 = ImageDraw.Draw(__self__.image2)
        __self__.draw3 = ImageDraw.Draw(__self__.image3)

        
        __self__.dict_row = {
            'red' : __self__.arrow_red,
            'green' : __self__.arrow_green,
            'white_bar' : __self__.white_bar
        }
        
    def make_image1(__self__, data: pd.DataFrame):
        
        df = data[data['image'] == 'image1']
        
        montserrat_small = __self__.montserrat_small
        draw = __self__.draw
        image = __self__.image

        dict_row = {
            'red' : __self__.arrow_red,
            'green' : __self__.arrow_green,
            'white_bar' : __self__.white_bar
        }
        
        ibov = df[df.index == '^BVSP']
        sp500 = df[df.index == '^GSPC']
        dolar = df[df.index == 'BRL=X']
        
        draw.text(xy=(325,705), text = ibov['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw.text(xy=(320,1020), text = sp500['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw.text(xy=(320,1340), text = dolar['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small) 

        # Changes
        draw.text(xy=(710,660), text = ibov['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw.text(xy=(710,975), text = sp500['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw.text(xy=(710,1295), text = dolar['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)

        image.paste(dict_row[ibov['test'].iloc[0]], (950,660), dict_row[ibov['test'].iloc[0]]) 
        image.paste(dict_row[sp500['test'].iloc[0]],(950,975), dict_row[sp500['test'].iloc[0]])
        image.paste(dict_row[dolar['test'].iloc[0]],(950,1295), dict_row[dolar['test'].iloc[0]])
        
        image.save('./assets/generated/1.png')
        
    def make_image2(__self__, data: pd.DataFrame):
        
        montserrat_extrabold = __self__.montserrat_extrabold
        montserrat_giant = __self__.montserrat_giant
        draw2 = __self__.draw2
        image2 = __self__.image2

        dict_row = {
            'red' : __self__.arrow_red,
            'green' : __self__.arrow_green,
            'white_bar' : __self__.white_bar
        }
        
        list_tickets = data.index.tolist()
        list_changes = data['change'].tolist()
        list_tests = data['test'].tolist()
        
        # Nomes
        draw2.text(xy=(215,508), text = list_tickets[0], fill = (255, 255, 255), font = montserrat_extrabold)
        draw2.text(xy=(215,659), text = list_tickets[1], fill = (255, 255, 255), font = montserrat_extrabold)
        draw2.text(xy=(215,811), text = list_tickets[2], fill = (255, 255, 255), font = montserrat_extrabold)
        draw2.text(xy=(215,1207), text = list_tickets[3], fill = (255, 255, 255), font = montserrat_extrabold)
        draw2.text(xy=(215,1360), text = list_tickets[4], fill = (255, 255, 255), font = montserrat_extrabold)
        draw2.text(xy=(215,1510), text = list_tickets[5], fill = (255, 255, 255), font = montserrat_extrabold)

        # Changes
        draw2.text(xy=(550,508), text = list_changes[0], fill = (255, 255, 255), font = montserrat_giant)
        draw2.text(xy=(550,659), text = list_changes[1], fill = (255, 255, 255), font = montserrat_giant)
        draw2.text(xy=(550,811), text = list_changes[2], fill = (255, 255, 255), font = montserrat_giant)
        draw2.text(xy=(550,1207), text = list_changes[3], fill = (255, 255, 255), font = montserrat_giant)
        draw2.text(xy=(550,1360), text = list_changes[4], fill = (255, 255, 255), font = montserrat_giant)
        draw2.text(xy=(550,1510), text = list_changes[5], fill = (255, 255, 255), font = montserrat_giant) 

        # High
        image2.paste(dict_row[list_tests[0]],(850,508), dict_row[list_tests[0]])  
        image2.paste(dict_row[list_tests[1]],(850,659), dict_row[list_tests[1]])
        image2.paste(dict_row[list_tests[2]],(850,811), dict_row[list_tests[2]])

        # Low
        image2.paste(dict_row[list_tests[3]],(850,1207), dict_row[list_tests[3]])
        image2.paste(dict_row[list_tests[4]],(850,1360), dict_row[list_tests[4]])
        image2.paste(dict_row[list_tests[5]],(850,1510), dict_row[list_tests[5]])
        
        image2.save('./assets/generated/2.png')
        
    
    def make_image3(__self__, data: pd.DataFrame):
        
        df = data[data['image'] == 'image3']
        
        montserrat_small = __self__.montserrat_small
        draw3 = __self__.draw3
        image3 = __self__.image3
        
        dict_row = __self__.dict_row
        
        btc = df[df.index == 'BTC-USD']
        eth = df[df.index == 'ETH-USD']
        gold = df[df.index == 'GC=F']
        oil = df[df.index == 'CL=F']
        
        draw3.text(xy=(275,460), text = btc['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw3.text(xy=(275,685), text = eth['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw3.text(xy=(275,1150), text = gold['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw3.text(xy=(275,1370), text = oil['price'].iloc[0], fill = (30, 63, 116), font = montserrat_small)

        draw3.text(xy=(730,420), text = btc['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw3.text(xy=(730,645), text = eth['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small) 
        draw3.text(xy=(730,1115), text = gold['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)
        draw3.text(xy=(730,1325), text = oil['change'].iloc[0], fill = (30, 63, 116), font = montserrat_small)

        image3.paste(dict_row[btc['test'].iloc[0]],(945,420), dict_row[btc['test'].iloc[0]])
        image3.paste(dict_row[eth['test'].iloc[0]],(945,635), dict_row[eth['test'].iloc[0]])
        image3.paste(dict_row[gold['test'].iloc[0]],(945,1115), dict_row[gold['test'].iloc[0]])
        image3.paste(dict_row[oil['test'].iloc[0]],(945,1325), dict_row[oil['test'].iloc[0]])
        
        image3.save('./assets/generated/3.png')
