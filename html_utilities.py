def outputHTMLDocument(htmlDocument, fileName, htmlExportPath='K:\\'):
    htmlDoc = open('%s%s.html' % (htmlExportPath, fileName), 'w')
    numBytes = htmlDoc.write(htmlDocument) # Just to stifle the return
    print('Created HTML Document at %s%s.html' % (htmlExportPath, fileName))
    htmlDoc.close()
