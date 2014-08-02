"""Our web wrapper for ABBYY OCR API. The convertFileToText method
takes a file to convert and returns the OCR recognized text as a 
string. The MainPage class demoes as a web app."""

import webapp2
import process

def convertFileToText(sourceFile):
    targetFile = 'delete.txt'
    language = 'English'
    outputFormat = 'txt'
    process.recognizeFile( sourceFile, targetFile, language, outputFormat )


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        print process.someFunction()
        sourceFile = 'jessie_deathcert.png'
        self.response.write(convertFileToText(sourceFile))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
