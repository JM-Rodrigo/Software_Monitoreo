package servidor;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.image.BufferedImage;
import java.net.ServerSocket;
import java.net.Socket;
import javax.imageio.ImageIO;

public class CompartirServidor {
    public static void main(String[] args) throws Exception {
        // Crea un objeto Robot para obtener una captura de pantalla del escritorio
        Robot robot = new Robot();  
        // resolución de intercepción
        Rectangle rec = new Rectangle(1366, 768);
        // puerto de escucha del servidor esperando conexión
        ServerSocket ss = new ServerSocket(8888);
        while(true){
            try{
                // Conéctese con éxito para obtener el socket
            Socket so = ss.accept();
            //Captura de pantalla
            BufferedImage bi = robot.createScreenCapture(rec);
            // Enviar a la salida
            ImageIO.write(bi, "png", so.getOutputStream());
            so.getOutputStream().flush();
            so.getOutputStream().close();
            so.close();
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }
    
}
