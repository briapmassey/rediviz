#importing dependencies
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph,Frame, SimpleDocTemplate
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch #for fonts
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('Roboto-Regular', 'Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Medium', 'Roboto-Medium.ttf'))
title_style= ParagraphStyle('My Para Style',fontName='Roboto-Medium',textColor=colors.HexColor("#C06291"), backColor='#FFFFFF', spaceBefore=0,fontSize=18)
text_style= ParagraphStyle('My Para Style', fontName='Roboto-Regular',textColor=colors.HexColor("#333333"), backColor='#FFFFFF', spaceBefore=10,leading=18,fontSize=15)

def editContentBlock(pic,title_text, text,textframe_x, textframe_y, textframe_width, textframe_height, pic_x, pic_y, pic_width, pic_height):
    editPicture(pic,pic_x, pic_y, pic_width, pic_height)
    editText(textframe_x, textframe_y, textframe_width, textframe_height, title_text, text)

def editPicture(pic, pic_x, pic_y, pic_width, pic_height):
    can.drawImage(pic,pic_x, pic_y, pic_width, pic_height)

def editText(x, y, width, height, title_text, text):
    can.setFillColorRGB(255,255,255)
    can.rect(x,y,width,height,fill=1,stroke=0)

    styles=getSampleStyleSheet()
    frame=Frame(x,y,width,height,showBoundary=0,leftPadding=0,
                           rightPadding=0,
                           topPadding=0,
                           bottomPadding=0
                           )

    p_text=Paragraph(title_text, title_style)
    p_text2=Paragraph(text, text_style)
    flow_obj=[p_text, p_text2]
    frame.addFromList(flow_obj,can)

def editTitleStyle(font_name, text_color, back_color, space_before, font_size):
    global title_style
    title_style= ParagraphStyle('My Para Style', fontName=font_name,textColor=colors.HexColor(text_color), backColor=back_color, spaceBefore=space_before,fontSize=font_size)
def editTextStyle(font_name, text_color, back_color, space_before, font_size):
    global text_style
    text_style= ParagraphStyle('My Para Style', fontName=font_name,textColor=colors.HexColor(text_color), backColor=back_color, spaceBefore=space_before,fontSize=font_size)


#Creating a new PDF with Reportlab
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

#editContentBlock("columbia logo.png", 217, 30, 370,115, "Covid vaccine","The vaccine works by giving your immune system practice fighting off the virus without any risk of infection.")
#editPicture("barcode.png",217, 30, 370,115)
#editText(217, 30, 370,115, "Bria Title", "Nex Text")
#editTitleStyle('Roboto-Medium','#0000FF' , '#FFFFFF',0,50)
#editTextStyle('Roboto-Medium','#C06291' , '#FFFFFF', 0,50)
#editText(217, 30, 370,115, "Bria Title", "Nex Text")
editContentBlock("columbia logo.png","Covid vaccine","The vaccine works by giving your immune system practice fighting off the virus without any risk of infection.", 217, 30, 370,115, 27,26,178,120)
#editPicture("barcode.png",217, 100, 370,115)
can.save()

#Beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
#reading in existing PDF
existing_pdf = PdfFileReader(open("testvaccine.pdf", "rb"))
output = PdfFileWriter()
#Adding the "watermark" (which is the new pdf) on the existing page;

#get number of pages
num_pages = existing_pdf.getNumPages()
#add all pages to new pdf
for i in range(num_pages):
    output.addPage(existing_pdf.getPage(i))

page_you_want_to_change = 1
page = existing_pdf.getPage(page_you_want_to_change)
page.mergePage(new_pdf.getPage(0))

# page_you_want_to_change = 6
# page = existing_pdf.getPage(page_you_want_to_change)
# page.mergePage(new_pdf.getPage(0))
#Writing "output" to a real file
# output.addPage(page)
outputStream = open("NewVaccineTailoring_ENGLISH.pdf", "wb")
output.write(outputStream)
outputStream.close()
