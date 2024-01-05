import 'package:flutter/material.dart';
import 'package:simple/main.dart';

class MemberPage extends StatelessWidget {
  MemberPage({required this.username});

  final String username;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Welcome Member"),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Text(
                'Menu',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              leading: Icon(Icons.home),
              title: Text('Home'),
              onTap: () {
                Navigator.pop(context); // Close the drawer
              },
            ),
            ListTile(
              leading: Icon(Icons.person),
              title: Text('Profile'),
              onTap: () {
                Navigator.pop(context); // Close the drawer
                // Navigate to the profile page
                Navigator.push(context, MaterialPageRoute(builder: (context) => ProfilePage(username: username)));
              },
            ),
            ListTile(
              leading: Icon(Icons.exit_to_app),
              title: Text('Logout'),
              onTap: () {
                Navigator.pop(context); // Close the drawer
                showLogoutConfirmation(context);
              },
            ),
            // Add more items as needed
          ],
        ),
      ),
      body: Column(
        children: <Widget>[
          SizedBox(height: 40.0),
          Center(child: Text('Hello $username', style: TextStyle(fontSize: 20.0))),
          SizedBox(height: 40.0),
          customElevatedButton(
            child: Text("LogOut"),
            onPressed: () {
              showLogoutConfirmation(context);
            },
            textColor: Colors.white,
            color: Colors.red,
            padding: EdgeInsets.fromLTRB(40, 10, 40, 10),
          ),
        ],
      ),
    );
  }

  ElevatedButton customElevatedButton({
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

  void showLogoutConfirmation(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Logout Confirmation"),
          content: Text("Are you sure you want to logout?"),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
              child: Text("Cancel"),
            ),
            TextButton(
              onPressed: () {
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(builder: (context) => MyHomePage()),
                  (route) => false,
                );
              },

              child: Text("Logout"),
            ),
          ],
        );
      },
    );
  }
}

class ProfilePage extends StatelessWidget {
  ProfilePage({required this.username});

  final String username;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Profile Page'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'This is the Profile Page!',
              style: TextStyle(fontSize: 20),
            ),
            SizedBox(height: 20),
            Text(
              'Username: $username',
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
