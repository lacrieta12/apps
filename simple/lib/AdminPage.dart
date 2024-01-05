import 'package:flutter/material.dart';

class AdminPage extends StatelessWidget {

  AdminPage({required this.username});
  final String username;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Welcome Admin"),),
      body: Column(

        children: <Widget>[
          Padding(padding: EdgeInsets.only(top: 40.0)),
          Center(child: Text('Hello $username', style: TextStyle(fontSize: 20.0),)),

          Padding(padding: EdgeInsets.only(top: 40.0)),

          customRaisedButton(
            child: Text("LogOut"),
            onPressed: (){
              Navigator.pushReplacementNamed(context,'/MyHomePage');
            }, textColor: Colors.white,
                color: Colors.red,
                padding: EdgeInsets.fromLTRB(40, 10, 40, 10),
          ),
        ],
      ),

    );
  }
  
  ElevatedButton customRaisedButton({
  required Widget child,
  required VoidCallback onPressed,
  required EdgeInsets padding,
  required Color textColor,
  required Color color,
}) {
  return ElevatedButton(
    onPressed: onPressed,
    style: ElevatedButton.styleFrom(
      foregroundColor: textColor, backgroundColor: color, padding: padding,
    ),
    child: child,
  );
}
}