#!/usr/bin/python3
import sys, smtplib
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
	smtpObj = smtplib.SMTP(server,port)
	try:
		check=smtpObj.ehlo() #ehlo, sup
		if int(check[0]) == 250:
			print("Conexão estabelefica")
			check=smtpObj.starttls()
			if int(check[0]) == 220:
				check=smtpObj.login(user, password)
				if int(check[0]) == 235:
					print("Login Efetuado com o usuário:", user)
					payload(smtpObj,user)
				else:
					print("Falha no login",check)
			else:
				print("Criptografia falhou: ", check)
		else:
			print("error in thelo")
	except Exception as error:
		print("Erou: ", error)

def close(Obj):
	check=Obj.quit()
	if int(check[0])==221:
		print("Conexão fechada com sucesso")
	else:
		print("Conexão fechada com falhas, but who cares")
def payload(smtpObj,user):
	print("Enviando ..")
	dst='EMAIL DST HERE'; payload='''Sup, i'm just testing my script, please, awnser this email, i need to know if this shit works'''
	smtpObj.sendmail(user,dst, str('Subject: teste\n'+ payload))
	close(smtpObj)	
	
def main():
	port=587;server=''
	if len(sys.argv) <= 1:
		while len(server) < 1:
			try:
				server=input('Server: ')
			except KeyboardInterrupt:
				sys.exit(0)
		port=input("Port[587]: ")
		con('smtp-mail.outlook.com', 587, '<EMAIL EHRE >', str(input("Password: ")))
	else:
		con('smtp-mail.outlook.com', 587, '<OR HERE>', str(input("Password: ")))
#		con(server,port,user,passw)

main()
