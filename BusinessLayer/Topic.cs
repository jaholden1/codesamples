using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    [Table("MLWWEB.PUBLIC_COMMENT_TOPICS")]
    public class TopicDB
    {
        [Key]
        public string TOPIC_ID { get; set; }
        public string TOPIC_DESCRIPTION { get; set; }
        public string PROJECT_NAME { get; set; }
        public string PROJECT_CONTACT { get; set; }
        public string PROJECT_EMAIL { get; set; }
        public DateTime? BEGIN_DATE { get; set; }
        public DateTime?  END_DATE { get; set; }      

    }
}
