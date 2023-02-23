from subprocess import Popen, PIPE
from documentcloud.addon import AddOn, SoftTimeOutAddOn

class Reflow(SoftTimeOutAddOn):
    """An Add-On that uses k2pdfopt to re-flow a PDF to make it easier to read on e-readers and smartphones"""
    def main(self):
        height = self.data["height"]
        width = self.data["width"]
        ppi = self.data["ppi"]
        self.set_message("Starting to re-flow documents...")
        for document in self.get_documents():
            self.set_message(f"Reflowing {document.title}...")
            process = Popen([f"k2pdfopt {document.title}.pdf -w {height} -h {width} -dpi {ppi} -idpi -2 -x"], stdin=PIPE, shell=True)
            process.communicate(input='\n'.encode('utf-8'))
            self.set_message("Uploading reflowed PDF")
            self.client.documents.upload(f"{document.title}_k2opt.pdf")

if __name__ == "__main__":
    Reflow().main()
