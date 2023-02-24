import os
from subprocess import Popen, PIPE
from documentcloud.addon import AddOn, SoftTimeOutAddOn

class Reflow(SoftTimeOutAddOn):
    """An Add-On that uses k2pdfopt to re-flow a PDF to make it easier to read on e-readers and smartphones"""
    def main(self):
        height = self.data["height"]
        width = self.data["width"]
        dpi = self.data["dpi"]
        self.set_message("Starting to re-flow documents...")
        for document in self.get_documents():
            # remove white space from document title for commandline to parse input appropriately
            pdf_name = f"'{document.title}'"
            with open(f"{pdf_name}.pdf", "wb") as file:
                file.write(document.pdf)
            self.set_message(f"Reflowing {document.title}...")
            process = Popen([f"k2pdfopt {pdf_name}.pdf -w {height} -h {width} -dpi {dpi} -idpi -2 -x"], stdin=PIPE, stdout=open(os.devnull, 'w'), shell=True)
            process.communicate(input='\n'.encode('utf-8'))
            self.set_message("Uploading reflowed PDF")
            self.client.documents.upload(f"{pdf_name}_k2opt.pdf")

if __name__ == "__main__":
    Reflow().main()
