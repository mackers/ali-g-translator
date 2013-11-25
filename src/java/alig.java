import java.awt.*;
import java.awt.event.*;

public class alig extends Frame implements ActionListener {

private TextArea inArea,outArea;
private Button translateButton;
private Translator T;

public alig() {
  setTitle("Da Ali G Translator");
  setBackground(Color.black);
  setForeground(Color.yellow);
  setLayout(new FlowLayout(FlowLayout.CENTER,10,10));
  
  //Label l = new Label("Loading... Please Wait");
  //add (l);
  T = new Translator();
  //remove (l);
  inArea = new TextArea("",7,20,TextArea.SCROLLBARS_VERTICAL_ONLY);
  add (inArea);
  translateButton = new Button("Translate");
  add (translateButton);
  translateButton.addActionListener(this);
  outArea = new TextArea("",7,20,TextArea.SCROLLBARS_VERTICAL_ONLY);
  add (outArea);
  add (new Label("www.mackers.com/alig"));
}

public static void main(String[] args) {
  Frame f = new alig();
  f.setSize(200,370);
  f.setVisible(true);
  f.addWindowListener(new WindowAdapter () {
	public void windowClosing(WindowEvent e) {
		System.exit(0);
	}
  });
}

public void actionPerformed(ActionEvent e) {
  if (e.getSource() == translateButton) {
    outArea.setText(T.translateSentence(inArea.getText()));
  }
}

}