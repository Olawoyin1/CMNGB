# from celery import shared_task
# import requests
# from decouple import config

# BREVO_API_KEY = config("BREVO_API_KEY")
# SENDER_EMAIL = config("SENDER_EMAIL")

# @shared_task
# def send_welcome_email(email, username):
#     subject = "Welcome to CareermatterNG! 🎉"
#     to_email = email  # recipient's email
#     body = f"""
#     Hi {username},

#     Welcome to CareermatterNG – Nigeria’s trusted freelance, contract, and remote job platform.

#     You can now create your profile, apply to jobs, or post projects.

#     Get started: https://careermatterng.com/dashboard

#     Cheers,
#     The CareermatterNG Team
#     """

#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; padding: 20px; color: #333;">
#         <div style="background-color: #ffffff; max-width: 600px; margin: auto; border-radius: 12px; padding: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2 style="color: #000080; margin-bottom: 16px; font-weight: bold;">Welcome to CareermatterNG, {username}!</h2>
#             <p style="line-height: 1.6;">We’re thrilled to have you on board. Whether you’re a freelancer seeking exciting projects, or a client looking for top talent – CareermatterNG is built to support your journey.</p>
#             <p style="line-height: 1.6;">Here’s what you can do:</p>
#             <ul style="line-height: 1.6; padding-left: 20px; list-style-type:none;">
#                 <li>✅ Build your professional profile</li>
#                 <li>✅ Browse or post jobs</li>
#                 <li>✅ Submit and manage proposals</li>
#                 <li>✅ Connect with trusted professionals and clients</li>
#             </ul>

#             <a href="https://careersng.netlify.app/login" style="display: inline-block; padding: 12px 24px; background-color: ##F2F2F2; color: #333333; border: none; text-decoration: none; border-radius: 6px; margin-top: 20px; font-weight: bold;">Go to Dashboard 🚀</a>

#             <div style="margin-top: 40px; font-size: 12px; color: #BEBCBC; text-align: center;">
#                 You're receiving this email because you signed up for CareermatterNG.<br/>
#                 Need help? <a href="mailto:support@careermatterng.com" style="color: #000080;">Contact our support team</a>.
#             </div>
#         </div>
#     </body>
#     </html>
#     """

#     # Brevo (Sendinblue) API endpoint
#     url = "https://api.brevo.com/v3/smtp/email"
#     headers = {
#         "api-key": BREVO_API_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {
#         "sender": {
#             "name": "CareermatterNG",
#             "email": SENDER_EMAIL
#         },
#         "to": [{"email": to_email}],
#         "subject": subject,
#         "textContent": body,
#         "htmlContent": html_content
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data, timeout=10)
#         response.raise_for_status()  # Check if the request was successful
#     except requests.exceptions.RequestException as e:
#         print(f"❌ ERROR: {e}")


from celery import shared_task
import requests
from decouple import config

BREVO_API_KEY = config("BREVO_API_KEY")
SENDER_EMAIL = config("SENDER_EMAIL")


@shared_task
def send_welcome_email(email, username):
    """
    Sends a personalized and detailed welcome email to newly registered users on CareermatterNG
    using the Brevo (Sendinblue) transactional email API.
    """
    subject = "Welcome to CareermatterNG! 🚀"
    recipient_email = email

    text_body = f"""
    Hi {username},

    Welcome to CareermatterNG – Nigeria’s trusted freelance, contract, and remote job platform.

    We’re excited to have you join a vibrant community of talented professionals and visionary businesses.
    Whether you're looking to find your next big project or hire top talent, you're in the right place.

    Here’s what you can do next:
    - Set up a standout profile that showcases your skills
    - Search and apply for freelance, remote, and contract jobs
    - Connect with clients and grow your career or business
    - Manage your proposals and projects easily through our platform

    Ready to get started? Visit your dashboard to explore opportunities tailored for you.

    👉 https://careermatterng.com/dashboard

    Need help or have questions? Our support team is just an email away: support@careermatterng.com

    Cheers,  
    The CareermatterNG Team
    """

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f7f7f7; padding: 40px 0px;  ; color: #333;">
            <div style="background-color: #ffffff; max-width: 600px;  margin: auto; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">

            <h2 style="color: #000080; font-weight: bolder; margin-bottom: 20px;">Welcome to CareermatterNG, {username}!</h2>
            <p style="font-size: 16px; line-height: 1.8;">We’re thrilled to have you on board. You are now part of a community built for passionate freelancers, remote workers, and businesses seeking exceptional talent across Nigeria and beyond.</p>

            <p style="font-size: 16px; line-height: 1.8; list-style-type:none;">As a member, you can:</p>
            <ul style="font-size: 16px; line-height: 1.8; padding-left: 20px; list-style-type: none;">
                <li>✅ Create a professional profile to showcase your skills and experience</li>
                <li>✅ Browse hundreds of freelance, contract, and remote job listings</li>
                <li>✅ Submit and manage proposals</li>
                <li>✅ Connect with trusted professionals and clients</li>
            </ul>

            <p style="font-size: 16px; line-height: 1.8;">Start your journey with us today:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="https://careermattersng.netlify.app/login" style="background-color: #05057a; color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    Go to Your Dashboard 🚀
                </a>
            </div>

            <p style="font-size: 16px; line-height: 1.8;">Need any assistance? Our friendly support team is ready to help. Reach us directly at <a href="mailto:support@careermatterng.com" style="color: #000080aa;">support@careermatterng.com</a>.</p>



            <hr style="margin: 40px 0; border: none; border-top: 1px solid #e0e0e0;" />
            <p style="font-size: 12px; color: #888888; text-align: center;">
                You are receiving this email because you registered an account on CareermatterNG.<br/>
                If you did not initiate this registration, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """



    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "sender": {
            "name": "CareermatterNG",
            "email": SENDER_EMAIL
        },
        "to": [{"email": recipient_email}],
        "subject": subject,
        "textContent": text_body,
        "htmlContent": html_body
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Welcome email successfully sent to {recipient_email}")
    except requests.exceptions.RequestException as error:
        print(f"❌ Failed to send welcome email to {recipient_email}: {error}")
