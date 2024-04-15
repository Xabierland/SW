package servlets;


import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;


public class CreateCollection extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de listResource");
		eXist = new HTTPeXist("http://localHost:8080");
		System.out.println("---> Saliendo de init()de LoginServlet");
	}
	
 
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
				
        String collection = request.getParameter("collection");

        // Create a new collection
        int collectionCreated = eXist.create(collection);

        if (collectionCreated == 200) {
            // Collection created successfully
            System.out.println("Collection created: " + collection);
            
            System.out.println("Redirecting to index.jsp");
            RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
            rd.forward(request, response);
        } else {
            // Failed to create collection
            System.out.println("Failed to create collection: " + collection);
            // Handle the error accordingly
        }

	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}
	
}

