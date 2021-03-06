import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;


public class ReadPropsFile {
    /** The Constant NETWORK_PROPERTIES_FILENAME. */
    public final static String NETWORK_PROPERTIES_FILENAME = "network.props";

    private String host = "";
    private int port = 0;
    private int os = 0;

    public ReadPropsFile(){
        readeProps();
    }

    /**
     * @author Fernando Barbosa Silva
     *  Method reads the network props file and set the variables host and port
     */
    private  void readeProps() {

        // Read network.props file to obtain host and port to connect to.
        try (InputStream fileStream = new FileInputStream(NETWORK_PROPERTIES_FILENAME)) {

            Properties props = new Properties();
            props.load(fileStream);
            this.host = props.getProperty("host");
            this.port = Integer.parseInt(props.getProperty("port"));
            this.os   = Integer.parseInt(props.getProperty("os"));

        } catch (FileNotFoundException e1) {
            System.out.println(e1.getMessage());
        } catch (IOException e2) {
            System.out.println(e2.getMessage());
        }
    }

    /**
     * @author Fernando
     * Get the host address from the props file.
     * @return  a string with the address.
     */
    public String getHost() {
        return host;
    }

    /**
     * @author Fernando
     * Get the prot number from the props file.
     * @return  port number in a integer type.
     */
    public int getPort() {
        return port;
    }

    /**
     * @author Fernando
     * Get the OS number from the props file "Windows = 0" "MACOS = 1"
     * @return  port number in a integer type.
     */
    public int getOs() {
        return os;
    }

}




