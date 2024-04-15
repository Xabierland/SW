package servlets;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;

public class DeleteSvg extends HttpServlet {
    private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de listResource");
		eXist = new HTTPeXist("http://localHost:8080");
		System.out.println("---> Saliendo de init()de LoginServlet");
	}

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String collection= request.getParameter("collection");
        String svgName = request.getParameter("svgName");
        
        //HTTPeXist eXist = new HTTPeXist("http://localHost:8080");
        String imagenSVG= eXist.read(collection, svgName);
        
        // Delete the image from the database
        eXist.delete(collection, svgName);

        // Redirect to the list of images
        response.sendRedirect("/GestorSvg/apiLR?collection=" + collection);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}
}
