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

def textbox(pic,x, y, width, height, title_text, text):
    can.drawImage(pic,x-178-12,y-4,178,120)
    can.setFillColorRGB(255,255,255)
    can.rect(x,y,width,height,fill=1,stroke=0)
    title_Style_new= ParagraphStyle('My Para Style', fontName='Roboto-Medium',textColor=colors.HexColor("#C06291"), backColor='#FFFFFF', spaceBefore=0,fontSize=18)
    my_Style_new= ParagraphStyle('My Para Style', fontName='Roboto-Regular',textColor=colors.HexColor("#333333"), backColor='#FFFFFF', spaceBefore=10,leading=18,fontSize=15)

    styles=getSampleStyleSheet()
    frame=Frame(x,y,width,height,showBoundary=0,leftPadding=0,
                           rightPadding=0,
                           topPadding=0,
                           bottomPadding=0
                           )

    p_text=Paragraph(title_text, title_Style_new)
    p_text2=Paragraph(text, my_Style_new)
    flow_obj=[p_text, p_text2]
    frame.addFromList(flow_obj,can)

#Creating a new PDF with Reportlab
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

textbox("columbia logo.png", 217, 30, 370,115, "Covid vaccine","The vaccine works by giving your immune system practice fighting off the virus without any risk of infection.")
can.save()

#Beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
#reading in existing PDF
existing_pdf = PdfFileReader(open("VaccinacionTailoring_ENGLISH.pdf", "rb"))
output = PdfFileWriter()
#Adding the "watermark" (which is the new pdf) on the existing page;
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
#Writing "output" to a real file
output.addPage(page)
outputStream = open("NewVaccineTailoring_ENGLISH.pdf", "wb")
output.write(outputStream)
outputStream.close()
