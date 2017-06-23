using comments.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using BusinessLayer;
using System.Configuration;


// the link to this application must provide two parameters.
// method =
// topicID = 
// method will be either Comment or Subscribe
// topicID will be topic id provided in mlwweb. (ex. krpua_scope)
// copy and paste into url for reference: ?method=Comment&topicID=krpua_scope 

namespace comments.Controllers
{
    public class HomeController : Controller
    {
        [HttpGet]
        public ActionResult Index(string method, string topicID)
            
        {
            Session["url"] = ConfigurationManager.AppSettings["env"];
            try
            {
                // set comment_id based on UUID
                Guid comment_id = System.Guid.NewGuid();
                Session["comment_id"] = comment_id;

                // get list of US states
                var states = States.GetAllStates();

                // instantiate Contact model
                var model = new Contact();

                // set StatesList equal to SelectListItems
                model.StatesList = States.GetSelectListItems(states);

                ContactContext contactcontext = new ContactContext();
                TopicDB topicdb = contactcontext.TopicInfo.Single(con => con.TOPIC_ID == topicID);

                // display form type based on url vars
                Session["method"] = method;
                Session["topicID"] = topicID;
                Session["topic"] = topicdb.TOPIC_DESCRIPTION;
                Session["project"] = topicdb.PROJECT_NAME;
                Session["contact"] = topicdb.PROJECT_CONTACT;
                Session["email"] = topicdb.PROJECT_EMAIL;

                return View(model);
            }
                              
            catch 
            {
                return RedirectToAction("error");
            }

        }

        [HttpPost]
        public ActionResult Index(Contact contact, string submitButton)
        {
            switch (submitButton)
            {
                case "Edit":
                    // get list of US states
                    var states = States.GetAllStates();

                    // set StatesList equal to SelectListItems
                    contact.StatesList = States.GetSelectListItems(states);

                    // return Index view with values
                    return View(contact);

                case "Submit":
                    // Need method & comment_id vars for database insertion
                    string method = Session["method"].ToString();
                    string comment_id = Session["comment_id"].ToString();
                    string topicID = Session["topicID"].ToString();

                    //convert state to two chars
                    string state = States.GetStateByName(contact.STATE);

                    // insert comment/subscriber to database
                    CommentsBusinessLayer commentsbusinesslayer = new CommentsBusinessLayer();
                    commentsbusinesslayer.AddComment(contact, method, comment_id, state, topicID);
                    if (Session["method"].ToString() == "Comment")
                    { 
                    return RedirectToAction("Index", "Complete");
                    }
                    else
                    {
                        return RedirectToAction("Subscribe", "Complete");
                    }
                default:
                    return View(contact);
            }
        }       

        [HttpPost]
        public ActionResult Review(Contact contact, FormCollection formcollection)
        {
            // review contact info
            contact.STATE = formcollection["StatesList"]; 
            return View(contact);
        }

        public ActionResult Error()
        {
            // params were not passed into Index.(for testing)
            return View();
        }
    }
    }