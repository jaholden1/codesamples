using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace comments.Models
{
    public class ContactContext : DbContext
    {
        public DbSet<BusinessLayer.ContactDB> ContactInput { get; set; }
        public DbSet<BusinessLayer.TopicDB> TopicInfo { get; set; }

    }
}