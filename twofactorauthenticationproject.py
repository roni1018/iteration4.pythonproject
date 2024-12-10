import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#function to generate a new secret key (done once for the user)
def generate_secret():
    totp = pyotp.TOTP(pyotp.random_base32()) #generates a random secret key
    print ("Your secret key (keep it safe):", totp.secret)
    return totp.secret

#function to generate the OTP based on the secret
def generate_otp(secret):
    totp = pyotp.TOTP(secret) #generates a random secret key
    otp = totp.now() #generates OTP based on the current time
    return otp

#function to send OTP via email
def send_email(otp, to_email):
    #set up the SMTP server
    from_email = "your-email@example.com" #your email
    from_password = "your-email-password" #your email password
    smtp_server = "smtp.gmail.com" #SMTP server
    smtp_port = 587 #the port being used for sending emails
    
    #set up the email content
    subject = "Your OTP for Two-Factor Authentication"
    body = f"Your OTP is: {otp}. IT will expire in 1 minute."
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    #sending the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() #secure the connection
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"OTP sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        
#function to verify the OTP that the user gave
def verify_otp(secret, entered_otp):
    totp = pyotp.TOTP(secret)
    if totp.verify(entered_otp):
        print("OTP verified successfully!")
    else:
        print("Invalid OTP. Please attempt again")
        
#main flow to simulate the two-step authentication
def two_step_authentication():
    secret = generate_secret() #step1 generate the secret, done by the user only once
    
    otp = generate_otp(secret) #sept2 generate a OTP and send it through an email
    to_email = input("Enter your email to recieve OTP: ") #user's eamil
    send_email(otp, to_email)
    
    entered_otp = input("Enter the OTP you recieved: ") #step3 ask the user for the OTP they recieved in the email
    
    verify_otp(secret, entered_otp) #verify the OTPs match
    
    
if __name__ == "__main__":
    two_step_authentication() #run the program/authentication
    
    
    
    
    
    