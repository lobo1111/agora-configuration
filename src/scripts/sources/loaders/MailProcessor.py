import email
import imaplib
import os
import uuid
from base.Container import Container

class MailProcessor(Container):

    def checkMailbox(self):
        if self.initConnection():
            for mail in self.getNewMails():
                self.processMail(mail)
                self._logger.info('Mail processed')
            self.closeConnection()
        self._logger.info('All emails checked')

    def closeConnection(self):
        self.__connection.close()
        self.__connection.logout()

    def initConnection(self):
        host = self._properties.getProperty('emailHost')
        user = self._properties.getProperty('emailUser')
        password = self._properties.getProperty('emailPassword')
        self.__connection = imaplib.IMAP4_SSL(host)
        response, message = self.__connection.login(user, password)
        if response == 'OK':
            self._logger.info('Connection to GMail established')
            return True
        else:
            self._logger.error('Can\'t connect to GMail: ' + response + ':' + message)
            return False

    def getNewMails(self):
        newMailDir = self._properties.getProperty('emailNew')
        response, message = self.__connection.select(newMailDir)
        if response == 'OK':
            response, mails = self.__connection.search(None, '*')
            if response == 'OK':
                if mails != None and len(mails) >= 1 and mails[0] != '':
                    self._logger.info('Got new messages: ' + mails[0])
                    return mails[0].split()
            else:
                self._logger.warning('Can\'t download mails: ' + response + ':' + message)
        else:
            self._logger.warning('Can\'t download mails: ' + response + ':' + message)
        return []

    def processMail(self, mailid):
        response, data = self.__connection.fetch(mailid, '(RFC822)')
        if response == 'OK':
            email_body = data[0][1]
            message = email.message_from_string(email_body)
            self._logger.info('Processing email - From[' + message["From"] + '] - Subject:' + message['Subject'])
            self.downloadAttachments(message)
            self.moveEmailToProcessed(mailid)
        else:
           logger.warning('Can\'t fetch mail: ' + response + ':' + message)

    def moveEmailToProcessed(self, mailid):
        processedDir = self._properties.getProperty('emailProcessed')
        response, message = self.__connection.copy(mailid, processedDir)
        if response == 'OK':
            response, message = self.__connection.store(mailid, '+FLAGS.SILENT', '(\\Deleted)')
            if response != 'OK':
                self._logger.warning('Can\'t delete mail: ' + response + ':' + message)
        else:
            self._logger.warning('Can\'t archive mail: ' + response + ':' + message)

    def downloadAttachments(self, email):
        for part in email.walk():
            if self.isAttachment(part):
                self.saveFile(part.get_filename(), part.get_payload(decode=True))

    def isAttachment(self, part):
        if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
            return False
        else:
            return True

    def saveFile(self, filename, data):
        uniqueFilename = '' + str(uuid.uuid4()) + '.' + filename
        dir = self._properties.getProperty('xmlNewXMLs')
        destination = os.path.join(dir, uniqueFilename)
        if not os.path.isfile(destination):
            file = open(destination, 'wb')
            file.write(data)
            file.close()
            self._logger.info('Attachment saved: ' + filename)
        else:
            self._logger.warning('File already exists')