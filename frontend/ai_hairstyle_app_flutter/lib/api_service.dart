import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const String apiUrl = "http://155.230.235.47:8000/analyze-face-shape/";

  static Future<Map<String, dynamic>> predictFaceShape(File imageFile) async {
  try {
    var request = http.MultipartRequest('POST', Uri.parse(apiUrl))
      ..files.add(await http.MultipartFile.fromPath('file', imageFile.path));

    var response = await request.send();
    var responseBody = await response.stream.bytesToString();

    print('Response Status: ${response.statusCode}');
    print('Response Body: $responseBody');

    if (response.statusCode == 200) {
      return json.decode(responseBody);
    } else {
      throw Exception('Failed to get prediction: ${response.statusCode} - $responseBody');
    }
  } catch (e) {
    print('Error: $e');
    rethrow;
  }
}

}
