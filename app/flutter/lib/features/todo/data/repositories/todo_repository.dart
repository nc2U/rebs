import 'package:dio/dio.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../models/todo_model.dart';

class TodoRepository {
  final Dio _dio;

  TodoRepository(this._dio);

  /// 나의 할일 목록 조회 (미삭제 항목 기준)
  Future<List<TodoItem>> getTodos({int? userId}) async {
    final queryParams = <String, dynamic>{
      'soft_deleted': false,
    };
    if (userId != null) {
      queryParams['user'] = userId;
    }

    final response = await _dio.get(
      ApiEndpoints.todos,
      queryParameters: queryParams,
    );

    final data = response.data;
    List results;
    if (data is Map && data.containsKey('results')) {
      results = data['results'] as List? ?? [];
    } else if (data is List) {
      results = data;
    } else {
      results = [];
    }

    return results
        .whereType<Map>()
        .map((e) => TodoItem.fromJson(Map<String, dynamic>.from(e)))
        .toList();
  }

  /// 신규 할일 생성
  Future<TodoItem> createTodo({
    required String title,
    required int userId,
  }) async {
    final response = await _dio.post(
      ApiEndpoints.todos,
      data: {
        'title': title,
        'user': userId,
      },
    );
    final data = response.data;
    return TodoItem.fromJson(
      data is Map ? Map<String, dynamic>.from(data) : <String, dynamic>{},
    );
  }

  /// 할일 완료/미완료 토글 및 제목 수정
  Future<TodoItem> updateTodo({
    required int id,
    String? title,
    bool? completed,
  }) async {
    final data = <String, dynamic>{};
    if (title != null) data['title'] = title;
    if (completed != null) data['completed'] = completed;

    final url = ApiEndpoints.resolve(ApiEndpoints.todoDetail, {'id': id});
    final response = await _dio.patch(url, data: data);
    final respData = response.data;
    return TodoItem.fromJson(
      respData is Map ? Map<String, dynamic>.from(respData) : <String, dynamic>{},
    );
  }

  /// 할일 삭제 (soft_deleted 처리)
  Future<void> softDeleteTodo(int id) async {
    final url = ApiEndpoints.resolve(ApiEndpoints.todoDetail, {'id': id});
    await _dio.patch(url, data: {'soft_deleted': true});
  }

  /// 할일을 워크스페이스 업무(Issue)로 전환
  /// 서버에서 업무 생성 + 할일 완료 처리 + 업무 연결을 원자적으로 수행한다.
  Future<TodoConvertResult> convertToIssue({
    required int id,
    required int projectId,
    required String subject,
    String description = '',
  }) async {
    final url = ApiEndpoints.resolve(ApiEndpoints.todoConvertToIssue, {'id': id});
    final response = await _dio.post(
      url,
      data: {
        'project': projectId,
        'subject': subject,
        'description': description,
      },
    );
    final respData = response.data;
    return TodoConvertResult.fromJson(
      respData is Map ? Map<String, dynamic>.from(respData) : <String, dynamic>{},
    );
  }

  /// 할일 영구 삭제
  Future<void> deleteTodo(int id) async {
    final url = ApiEndpoints.resolve(ApiEndpoints.todoDetail, {'id': id});
    await _dio.delete(url);
  }
}
