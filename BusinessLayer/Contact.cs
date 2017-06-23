using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Mvc;

namespace BusinessLayer
{
    public class Contact
    {
        [Key]
        public string TOPIC_ID { get; set; }
        [Required]
        [DisplayName("First Name")]

        public string FIRST_NAME { get; set; }
        [DisplayName("Middle Name")]
        public string MIDDLE_NAME { get; set; }
        [Required]
        [DisplayName("Last Name")]
        public string LAST_NAME { get; set; }
        [DisplayName("Job Title")]
        public string TITLE { get; set; }
        [DisplayName("Agency/Business")]
        public string AGENCY { get; set; }
        [Required]
        [DisplayName("Mailing Address")]
        public string ADDRESS { get; set; }
        [Required]
        [DisplayName("City")]
        public string CITY { get; set; }
        [DisplayName("State")]
        public string STATE { get; set; }
        [Required]
        [DisplayName("Zip")]
        [RegularExpression(@"\d{5}-?(\d{4})?$", ErrorMessage = "Invalid Zip Code")]
        public string ZIP { get; set; }
        [DisplayName("Day Phone")]
        public string DAY_PHONE { get; set; }
        [DisplayName("Alternate Phone")]
        public string ALT_PHONE { get; set; }
        [DisplayName("Fax")]
        public string FAX { get; set; }
        [DisplayName("Email")]
        [EmailAddress(ErrorMessage = "Invalid Email Address")]
        public string EMAIL { get; set; }
        [DisplayName("Contact List")]
        public string CONTACT_LIST { get; set; }
        public string DATE_RECEIVED { get; set; }
        [DisplayName("Comment")]
        public string PUBLIC_COMMENT { get; set; }
        [Required]
        [DisplayName("State")]
        public IEnumerable<SelectListItem> StatesList { get; set; }
    }

    [Table("MLWWEB.V_PUBLIC_COMMENT_SUMMARY")]
    public class ContactDB
    {
        [Key]
        public string COMMENT_ID { get; set; }
        public string TOPIC_ID { get; set; }
        public string PROJECT_NAME { get; set; }
        public string TOPIC_DESCRIPTION { get; set; }
        [Required]
        [DisplayName("First Name")]
        public string FIRST_NAME { get; set; }
        [DisplayName("Middle Name")]
        public string MIDDLE_NAME { get; set; }
        [Required]
        [DisplayName("Last Name")]
        public string LAST_NAME { get; set; }
        [DisplayName("Job Title")]
        public string TITLE { get; set; }
        [DisplayName("Agency/Business")]
        public string AGENCY { get; set; }
        [Required]
        [DisplayName("Mailing Address")]
        public string ADDRESS { get; set; }
        [Required]
        [DisplayName("City")]
        public string CITY { get; set; }
        [DisplayName("State")]
        public string STATE { get; set; }
        [Required]
        [DisplayName("Zip")]
        public string ZIP { get; set; }
        [DisplayName("Day Phone")]
        public string DAY_PHONE { get; set; }
        [DisplayName("Alternate Phone")]
        public string ALT_PHONE { get; set; }
        [DisplayName("Fax")]
        public string FAX { get; set; }
        [DisplayName("Email")]
        public string EMAIL { get; set; }
        [DisplayName("Contact List")]
        public string CONTACT_LIST { get; set; }
        public string DATE_RECEIVED { get; set; }
        [DisplayName("Comment")]
        public string PUBLIC_COMMENT { get; set; }

}

}
