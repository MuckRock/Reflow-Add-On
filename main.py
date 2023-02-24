import os
from subprocess import Popen, PIPE
from documentcloud.addon import AddOn, SoftTimeOutAddOn

class Reflow(SoftTimeOutAddOn):
    """An Add-On that uses k2pdfopt to re-flow a PDF to make it easier to read on e-readers and smartphones"""
    project_id = None
    def check_permissions(self):
        """The user must be a verified journalist to upload a document"""
        self.set_message("Checking permissions...")
        user = self.client.users.get("me")
        if not user.verified_journalist:
            self.set_message(
                "You need to be verified to use this add-on. Please verify your "
                "account here: https://airtable.com/shrZrgdmuOwW0ZLPM"
            )
            sys.exit()
            
    def main(self):
        self.check_permissions()
        height = self.data["height"]
        width = self.data["width"]
        dpi = self.data["dpi"]
        access_level = self.data["access_level"]
        if "project_id" in self.data:
            self.project_id = self.data["project_id"]
        self.set_message("Starting to re-flow documents...")
        for document in self.get_documents():
            # Wrap title of document in whitespace for shell handling
            pdf_name = f"'{document.title}.pdf'"
            with open(f"{document.title}.pdf", "wb") as file:
                file.write(document.pdf)
            self.set_message(f"Reflowing {document.title}...")
            process = Popen([f"k2pdfopt {pdf_name} -w {height} -h {width} -dpi {dpi} -idpi -2 -x"], stdin=PIPE, shell=True)
            process.communicate(input='\n'.encode('utf-8'))
            self.set_message("Uploading reflowed PDF")
            self.client.documents.upload(f"{document.title}_k2opt.pdf", access=access_level)
            if self.project_id is not None:
                project = self.client.projects.get(id=self.project_id)
                project.documents.append(document)
                project.save()

if __name__ == "__main__":
    Reflow().main()
