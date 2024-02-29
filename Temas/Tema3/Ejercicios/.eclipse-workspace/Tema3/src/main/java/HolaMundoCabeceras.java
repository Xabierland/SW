import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HolaMundoCabeceras extends HttpServlet{

	public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
    	System.out.println("---> Entrando en servlet HolaMundoCabeceras"); ;
    	response.setContentType("text/plain; charset=utf-8");
    	
   		PrintWriter http_out = response.getWriter();
   		
		http_out.println("Cabeceras petici�n HTTP:");
		System.out.println("     Cabeceras petici�n HTTP:");
	 	Enumeration<String> headerNames = request.getHeaderNames();
	 	while (headerNames.hasMoreElements()) {
	 		String headerName = (String) headerNames.nextElement();
	 		String headerNameValue = headerName + ": " + request.getHeader(headerName);
	 		http_out.println("     " + headerNameValue);
	 		System.out.println("          " + headerNameValue);
    	}
    	
	 	System.out.println("---> Saliendo de servlet HolaMundoCabeceras");;
	}
}
