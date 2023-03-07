from gc import get_objects
from pypdf import PdfReader

def run():
    BE = r"C:\Daten\prog\verapdf\20230214081436_extract.pdf"
    SO = r"C:\Daten\prog\verapdf\CH857632820629.pdf"
    reader = PdfReader(SO)

    for page in reader.pages:
        for content in page['/Contents']:
            obj = content.get_object()

        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"]}
                print(annotation)

if __name__ == '__main__':
    run()