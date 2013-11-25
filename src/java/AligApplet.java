import java.awt.*;
import java.awt.event.*;
import java.applet.*;

public class AligApplet extends Applet implements ActionListener {

private TextArea inArea,outArea;
private Button translateButton;
private Translator T;

public void init() {
  setBackground(Color.black);
  setForeground(Color.yellow);
  if ((getCodeBase().toString().equals("http://mackers.com/alig/")) 
	  || (getCodeBase().toString().equals("http://www.mackers.com/alig/"))
	  || (getCodeBase().toString().indexOf("file:")!=-1)) {
    Label l = new Label("Loading... Please Wait");
    add (l);
    T = new Translator();
    remove (l);
    inArea = new TextArea("",7,20,TextArea.SCROLLBARS_VERTICAL_ONLY);
    inArea.setBackground(Color.black);
    add (inArea);
    translateButton = new Button("Translate");
    add (translateButton);
    translateButton.addActionListener(this);
    outArea = new TextArea("",7,20,TextArea.SCROLLBARS_VERTICAL_ONLY);
    outArea.setBackground(Color.black);
    add (outArea);
    add (new Label("www.mackers.com/alig"));
  } else {
	Label l = new Label("Da Ali G Translater: http://mackers.com/alig/");
	add (l);
  }
}

public void actionPerformed(ActionEvent e) {
  if (e.getSource() == translateButton) {
    outArea.setText(T.translateSentence(inArea.getText()));
  }
}

}