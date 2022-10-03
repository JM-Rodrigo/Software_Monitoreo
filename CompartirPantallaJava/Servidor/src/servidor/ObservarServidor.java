package servidor;
import java.awt.image.BufferedImage;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class ObservarServidor {
    public static void main(String[] args)   {
        // TODO Auto-generated method stub
        // Crear marco de visualización
        JFrame jf = new JFrame();
        jf.setSize(1366, 768);
        jf.setVisible(true);
        while(true){
            try{
                // Solicitar lado del servidor  
                Socket socket = new Socket("192.168.8.27",8888);
                // Obtener fotos
                BufferedImage bi = ImageIO.read(socket.getInputStream());
                JLabel lab = new JLabel();
                jf.setContentPane(lab);
                lab.setSize(1366, 768);
                ImageIcon ii = new ImageIcon(bi);
                // etiqueta muestra las imágenes recibidas del servidor
                lab.setIcon(ii);
                socket.close();
                // Dormir por un corto tiempo, puede ajustarse automáticamente
                Thread.sleep(10);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }
    
}
