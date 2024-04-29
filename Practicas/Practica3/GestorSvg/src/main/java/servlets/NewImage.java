package servlets;

import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import HTTPeXist.HTTPeXist;

public class NewImage extends HttpServlet {
    private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	
	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de NewImage");
		eXist = new HTTPeXist("http://localhost:8080");
		System.out.println("---> Saliendo de init()de NewImage");
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
	{
		String svgName = request.getParameter("svgName");
		String collection = request.getParameter("collection");

		// Create a new image
		int imageCreated = eXist.subirString(collection, "", svgName);

		if (imageCreated == 201) {
			// Image created successfully
			System.out.println("Image created: " + svgName);
			
			System.out.println("Redirecting to index.jsp");
			RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
			rd.forward(request, response);
		} else {
			// Failed to create image
			System.out.println("Failed to create image: " + svgName);
			// Handle the error accordingly
		}
	}

	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
	{
		doGet(request, response);
	}
}
