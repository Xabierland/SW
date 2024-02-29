import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HolaMundo extends HttpServlet 
{
	public void doGet(HttpServletRequest request, HttpServletResponse response)
		throws ServletException, IOException {
	System.out.println("---> Entering HolaMundo servlet"); // log
	PrintWriter out = response.getWriter();
	out.println("Hola Mundo");
	System.out.println("<--- Exiting HolaMundo servlet"); // log
	}
}