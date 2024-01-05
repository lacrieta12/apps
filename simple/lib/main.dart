import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'dart:async';
import 'dart:convert';

import 'AdminPage.dart';
import 'MemberPage.dart';

void main() {
  runApp(MyApp());
}

String username='';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      theme: buildTheme(),
      debugShowCheckedModeBanner: false,
      title: 'Login Localhost',
      home: MyHomePage(),
      routes: <String,WidgetBuilder>{
        '/AdminPage': (BuildContext context)=> AdminPage(username: username,),
        '/MemberPage': (BuildContext context)=> MemberPage(username: username,),
        '/MyHomePage': (BuildContext context)=> MyHomePage(),
      },
    );
  }
  
  ThemeData buildTheme() {
    final ThemeData base = ThemeData();
    return base.copyWith(
      hintColor: Colors.purple,
      primaryColor: Colors.yellow,
      inputDecorationTheme: InputDecorationTheme(
        hintStyle: TextStyle(
          color: Colors.blue,
        ),
        labelStyle: TextStyle(
          color: Colors.green,
        ),
      ),
    );
  }
}

// class MyAppState extends ChangeNotifier {
//   var current = WordPair.random();

//   void getNext() {
//     current = WordPair.random();
//     notifyListeners();
//   }
// }

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  TextEditingController user= TextEditingController();
  TextEditingController pass=TextEditingController();

  String msg='';


Future<void> _login() async {
  final response = await http.post(
    Uri.parse("http://192.168.43.235/flutter_login/login.php"),
    body: {
      "username": user.text,
      "password": pass.text,
    },
  );

  print("Response body: ${response.body}");

  try {
    List<dynamic> datauser = json.decode(response.body);

    if (datauser.isEmpty) {
      setState(() {
        msg = "Login Fail";
      });
    } else {
      Map<String, dynamic> userData = datauser[0];

      print("User Level: ${userData['level']}");

      setState(() {
        username = userData['username'];
      });

      if (userData['level'] == 'admin') {
        print("Navigating to AdminPage");
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => AdminPage(username: username)));
      } else if (userData['level'] == 'member') {
        print("Navigating to MemberPage");
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => MemberPage(username: username)));
      } else {
        print("Unknown user level: ${userData['level']}");
      }
    }
  } catch (e) {
    print("Error decoding JSON: $e");
    setState(() {
      msg = "Login failed. Invalid username or password.";
    });
  }
}







  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(title: Text("Login"),),

      body: Container(
        decoration: BoxDecoration(color: Colors.black),
//        margin: EdgeInsets.all(30),
        padding: const EdgeInsets.all(30.0),
        child: Center(
          child: Column(


            children: <Widget>[
              Padding(padding: EdgeInsets.only(top: 30.0)),

              Text('Login Here', style: TextStyle(
                    shadows: <Shadow>[
                      Shadow(
                        offset: Offset(1.0, 1.0),
                        blurRadius: 2.0,
                        color: Color.fromARGB(255, 0, 0, 0),
                      ),
                    ],
                  color: hexToColor("#F2A03D"), fontSize: 25.0),),

              Padding(padding: EdgeInsets.only(top: 50.0)),


              TextFormField(

                controller: user,
                decoration: InputDecoration(


                  enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25.0),
                      borderSide: BorderSide(color: Colors.red)
                  ),


                  labelText: "Username",
                  prefixIcon: const Icon(Icons.person, color: Colors.green,),
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(25.0),
                    borderSide: BorderSide(
                    ),
                  ),
                ),

                keyboardType: TextInputType.emailAddress,
                style: TextStyle(
                  fontFamily: "Poppins",
                  color: Colors.white,
                ),
              ),


              Padding(
                padding: EdgeInsets.all(30.0),
              ),

              TextFormField(
                controller: pass,
                obscureText: true,
                decoration: InputDecoration(
                  enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25.0),
                      borderSide: BorderSide(color: Colors.red)
                  ),
                  labelText: "Password",
                  prefixIcon: const Icon(Icons.remove_red_eye , color: Colors.green,),
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(25.0),
                    borderSide: BorderSide(
                    ),
                  ),
                ),

                style: TextStyle(
                  fontFamily: "Poppins",
                  color: Colors.white,
                ),
              ),

              Padding(
                padding: EdgeInsets.all(8.0),
              ),

              customRaisedButton(
                child: Text("Login"),
                onPressed: () {
                  _login();
                  },
                textColor: Colors.white,
                color: Colors.red,
                padding: EdgeInsets.fromLTRB(40, 10, 40, 10),
              ),

              Text(msg,style: TextStyle(fontSize: 20.0,color: Colors.red),)


            ],
          ),
        ),
      ),
    );
  }


    Color hexToColor(String code) {
      return Color(int.parse(code.substring(1, 7), radix: 16) + 0xFF000000);
    }
    
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
