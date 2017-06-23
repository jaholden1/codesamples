using Oracle.ManagedDataAccess.Client;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class CommentsBusinessLayer
    {
        public void AddComment(Contact contact, string method, string comment_id, string state, string topicID)
        {
            string connectionString2 = ConfigurationManager.ConnectionStrings["ContactContext"].ConnectionString;
            using (OracleConnection con = new OracleConnection(connectionString2))
            {
                OracleCommand cmd = new OracleCommand("Insert into MLWWEB.PUBLIC_COMMENT (COMMENT_ID, TOPIC_ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, TITLE, AGENCY, ADDRESS, CITY, STATE, ZIP, DAY_PHONE, ALT_PHONE, FAX, EMAIL, CONTACT_LIST, METHOD_RECEIVED, DATE_RECEIVED, COMPLETED, PUBLIC_COMMENT) VALUES(:COMMENT_ID, :TOPIC_ID, :FIRST_NAME, :MIDDLE_NAME, :LAST_NAME, :TITLE, :AGENCY, :ADDRESS, :CITY, :STATE, :ZIP, :DAY_PHONE, :ALT_PHONE, :FAX, :EMAIL, :CONTACT_LIST, :METHOD_RECEIVED, :DATE_RECEIVED, :COMPLETED, :PUBLIC_COMMENT)", con);
                cmd.Parameters.Add(new OracleParameter(":COMMENT_ID", comment_id));
                cmd.Parameters.Add(new OracleParameter(":TOPIC_ID", topicID));
                cmd.Parameters.Add(new OracleParameter(":FIRST_NAME", contact.FIRST_NAME));
                cmd.Parameters.Add(new OracleParameter(":MIDDLE_NAME", contact.MIDDLE_NAME));
                cmd.Parameters.Add(new OracleParameter(":LAST_NAME", contact.LAST_NAME));
                cmd.Parameters.Add(new OracleParameter(":TITLE", contact.TITLE));
                cmd.Parameters.Add(new OracleParameter(":AGENCY", contact.AGENCY));
                cmd.Parameters.Add(new OracleParameter(":ADDRESS", contact.ADDRESS));
                cmd.Parameters.Add(new OracleParameter(":CITY", contact.CITY));
                cmd.Parameters.Add(new OracleParameter(":STATE", state));
                cmd.Parameters.Add(new OracleParameter(":ZIP", contact.ZIP));
                if (contact.DAY_PHONE != null)
                { 
                cmd.Parameters.Add(new OracleParameter(":DAY_PHONE", Regex.Replace(contact.DAY_PHONE, "[^0-9a-zA-Z]+", "")));
                }
                else
                {
                cmd.Parameters.Add(new OracleParameter(":DAY_PHONE", contact.DAY_PHONE));
                }
                if (contact.ALT_PHONE != null)
                {
                    cmd.Parameters.Add(new OracleParameter(":ALT_PHONE", Regex.Replace(contact.ALT_PHONE, "[^0-9a-zA-Z]+", "")));
                }
                else
                {
                    cmd.Parameters.Add(new OracleParameter(":ALT_PHONE", contact.ALT_PHONE));
                }
                if (contact.FAX != null)
                {
                    cmd.Parameters.Add(new OracleParameter(":FAX", Regex.Replace(contact.FAX, "[^0-9a-zA-Z]+", "")));
                }
                else
                {
                    cmd.Parameters.Add(new OracleParameter(":FAX", contact.FAX));
                }
                cmd.Parameters.Add(new OracleParameter(":EMAIL", contact.EMAIL));
                cmd.Parameters.Add(new OracleParameter(":CONTACT_LIST", contact.CONTACT_LIST));
                cmd.Parameters.Add(new OracleParameter(":METHOD_RECEIVED", "Web " + method));
                cmd.Parameters.Add(new OracleParameter(":DATE_RECEIVED", DateTime.Now));
                cmd.Parameters.Add(new OracleParameter(":COMPLETED", "Y"));
                cmd.Parameters.Add(new OracleParameter(":PUBLIC_COMMENT", contact.PUBLIC_COMMENT));
                con.Open();
                cmd.ExecuteNonQuery();
            }
        }
    }
}
