using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Net.Mail;
using BusinessLayer;
using RazorEngine.Templating;
using comments.Models;
using System.Configuration;
using System.IO;
using iTextSharp.text;
using iTextSharp.text.pdf;
using iTextSharp.text.html.simpleparser;

namespace comments.Controllers
{
    public class CompleteController : Controller
    {
        // GET: Complete
        public ActionResult Index(Contact contact)
        {
            // send email to admin with PDF download
            var templateService = new TemplateService();
            string commentID = Session["comment_id"].ToString();

            // get comment info based on UUID
            ContactContext contactcontext = new ContactContext();
            ContactDB contactdb = contactcontext.ContactInput.Single(con => con.COMMENT_ID == commentID);

            // include email template
            var emailHtmlBody = templateService.Parse(System.IO.File.ReadAllText(Server.MapPath("~/Views/Email/Comment.cshtml")), contactdb, null, null);
            string body = emailHtmlBody;         
            MailMessage mail = new MailMessage();
            mail.To.Add(Session["email"].ToString());

            // remmed for testing
            // mail.CC.Add("dnr.dmlwweb@alaska.gov");
            mail.CC.Add("josetteserrill@gmail.com");
            mail.From = new MailAddress("dnr.dmlwweb@alaska.gov");
            mail.Subject = Session["project"].ToString() + " Public Comment Online";
            mail.Body = body;
            mail.IsBodyHtml = true;
            SmtpClient smtp = new SmtpClient();
            smtp.Host = "smtpa.state.ak.us";
            smtp.Port = 587;
            smtp.EnableSsl = true;
            smtp.Send(mail);

            return RedirectToAction("Comment");
        }
        public ActionResult Comment()
        {
            // display form results to user
            string commentID = Session["comment_id"].ToString();
            ContactContext contactcontext = new ContactContext();
            ContactDB contactdb = contactcontext.ContactInput.Single(con => con.COMMENT_ID == commentID);
            return View(contactdb);
        }
        public ActionResult Subscribe()
        {
            return View();
        }


        public ActionResult PDF(string comment_id)
        {
            // generate PDF for admin
            ContactContext contactcontext = new ContactContext();
            ContactDB contactdb = contactcontext.ContactInput.Single(con => con.COMMENT_ID == comment_id);
            var templateService = new TemplateService();

            // include PDF template here
            var HtmlBody = templateService.Parse(System.IO.File.ReadAllText(Server.MapPath("~/Views/Complete/Pdf.cshtml")), contactdb, null, null);
            string HTMLContent = HtmlBody;

            Response.Clear();
            Response.ContentType = "application/pdf";
            Response.AddHeader("content-disposition", "attachment;filename=" + "PublicComment.pdf");
            Response.Cache.SetCacheability(HttpCacheability.NoCache);
            Response.BinaryWrite(GetPDF(HTMLContent));
            Response.End();
            return View();
        }
        public byte[] GetPDF(string pHTML)
        {
            byte[] bPDF = null;

            MemoryStream ms = new MemoryStream();
            TextReader txtReader = new StringReader(pHTML);

            // 1: create object of a itextsharp document class
            Document doc = new Document(PageSize.A4, 25, 25, 25, 25);

            // 2: we create a itextsharp pdfwriter that listens to the document and directs a XML-stream to a file
            PdfWriter oPdfWriter = PdfWriter.GetInstance(doc, ms);

            // 3: we create a worker parse the document
            HTMLWorker htmlWorker = new HTMLWorker(doc);

            // 4: we open document and start the worker on the document
            doc.Open();
            htmlWorker.StartDocument();

            // 5: parse the html into the document
            htmlWorker.Parse(txtReader);

            // 6: close the document and the worker
            htmlWorker.EndDocument();
            htmlWorker.Close();
            doc.Close();

            bPDF = ms.ToArray();

            return bPDF;
        }
    }
}