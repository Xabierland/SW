import java.sql.*;


class JavaMySQLtest {

    public static void main (String [ ] args) {
    	
        String url = "jdbc:mysql://localhost:3306/";
        String user = "root";
        String passwd = "1094";
        String driver = "com.mysql.cj.jdbc.Driver";

        Connection conn = null;
        try {
            Class.forName(driver).newInstance();
            conn = DriverManager.getConnection(url, user, passwd);
            System.out.print("Reference of 'conn' object: ");
            System.out.println(conn);
        } catch(Exception e) {
            System.out.println("Exception: " + e.getMessage());
        }

        String query = "SELECT * FROM shareinfo.messages;";
        System.out.println("\nDB query: " + query);
        try {
            Statement st = conn.createStatement();
            ResultSet res = st.executeQuery(query);
            while(res.next()) {
                System.out.println(res.getString("username") + " >>> " + res.getString("message"));
            }
        } catch(Exception e) {
            System.out.println("Exception: " + e.getMessage());
        }
    }

}