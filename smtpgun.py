#!/usr/bin/python3
import sys, smtplib, getopt, csv
servers={
  'gmail': 'smtp.gmail.com',
  'hotmail':'smtp-mail.outlook.com',
  'outlook':'smtp-mail.outlook.com',
  'yahoo': 'smtp-mail.yahoo.com',
  'at&t':'smtp.mail.att.net', #porta465
  'comcast':'smtp.comcast.net',
  'verizon':'smtp.verizon.net'# porta 465
  }

def con(server,port,user,password):
  print("[+] Starting Connection with", server,port, "with user: ", user)
  smtpObj = smtplib.SMTP(server,port)
  try:
    check=smtpObj.ehlo() #ehlo, sup
    if int(check[0]) == 250:
      print("[+] Conexão estabelecida")
      check=smtpObj.starttls()
      if int(check[0]) == 220:
        check=smtpObj.login(user, password)
        if int(check[0]) == 235:
          print("[+] Login Efetuado com o usuário:", user)
          return smtpObj
        else:
                                    print("Falha no login: ", check)
      else:
        print("Criptografia falhou: ", check)
    else:
      print("error in ehlo")
  except Exception as error:
    print("Erou: ", error)

def close(Obj):
  check=Obj.quit()
  if int(check[0])==221:
    print("Conexão fechada com sucesso")
  else:
    print("Conexão fechada com falhas, but who cares")

def payload(smtpObj,user,mfile,field,dstfile):
  dstaddress=[]
  print("[+] Loading info from csv file:", mfile )
  with open(dstfile,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dstaddress.append(row[field])      
  print("[+] Loading payload")
  try:
    arq=open(mfile)
    payload=arq.read()
  except Exception as error:
      print("Error while reading the payload file:",error)
  for dst in dstaddress:
    print("[+] Sending mail to: ", dst)
    smtpObj.sendmail(user,dst, str('Subject: teste \n\n'+ payload))
  arq.close()
  close(smtpObj)

def usage():
    usage="""SMTPGUN a crash tutorial
    I will help you with the arguments bro, calm down morty!
        -u <username>: Set the username from smtp server
        -p <password>: Set the password from smtp server
        -s <server>: Set the server name, use FQDN here. Default is outlook
        -P <port> :Set the port of smtp server. Default is port 587 TCP
        -m <message file name>: Set the email file to send.
        -f <file with destinations> : Set the destinations of your email, use CSV files
        -F <field_of_mail>: Set the field inside csv wich is related to mail address
        Example:
    """
    usage+=str(sys.argv[0])+": -u yourMailaddress@domain.com -p YourPassword -F FildInsideCSVfile -f file.csv -m fileWithMessageToSend"
    print(usage)
    sys.exit(2)
  
def main(argv):
#  global servers
  port=587
  server=servers['hotmail']
  if len(sys.argv) <= 1:
      usage()
  try:
      opts,args = getopt.getopt(argv, "u:p:s:m:f:p:P:F:h")
  except getopt.GetoptError as err:
      print("Error in getopt:",err)
      usage()
  for o, a in opts:
      if o == "-u":
        mailaddress = a
      elif o == "-p":
        password = a
      elif o == "-P":
        port = a
      elif o == "-s":
        server = a
      elif o == "-m":
        mfile = a
      elif o == "-f":
        dstfile = a
      elif o == "-F":
        field = a
      elif o =="-h":
          usage()
      else:
          print("Error while reading options")
          usage()
  smtp = con(server,int(port), mailaddress, password)
  payload(smtp,mailaddress,mfile,field,dstfile)
if __name__ == "__main__":
    main(sys.argv[1:])
