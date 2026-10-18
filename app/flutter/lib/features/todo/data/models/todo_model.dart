import 'package:flutter/foundation.dart';

/// 할일이 업무(Issue)로 전환된 경우의 요약 정보 (백엔드 TodoIssueInfoSerializer 대응)
@immutable
class TodoIssueInfo {
  final int pk;
  final int projectId;
  final String projectSlug;
  final String projectName;
  final String subject;

  const TodoIssueInfo({
    required this.pk,
    required this.projectId,
    this.projectSlug = '',
    this.projectName = '',
    this.subject = '',
  });

  factory TodoIssueInfo.fromJson(Map<String, dynamic> json) {
    return TodoIssueInfo(
      pk: json['pk'] as int? ?? 0,
      projectId: json['project_id'] as int? ?? 0,
      projectSlug: json['project_slug'] as String? ?? '',
      projectName: json['project_name'] as String? ?? '',
      subject: json['subject'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'pk': pk,
      'project_id': projectId,
      'project_slug': projectSlug,
      'project_name': projectName,
      'subject': subject,
    };
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TodoIssueInfo &&
          runtimeType == other.runtimeType &&
          pk == other.pk &&
          projectId == other.projectId &&
          projectSlug == other.projectSlug &&
          projectName == other.projectName &&
          subject == other.subject;

  @override
  int get hashCode =>
      pk.hashCode ^
      projectId.hashCode ^
      projectSlug.hashCode ^
      projectName.hashCode ^
      subject.hashCode;
}

@immutable
class TodoItem {
  final int pk;
  final int user;
  final String title;
  final bool completed;
  final bool softDeleted;

  /// 전환된 업무(Issue) PK. 전환되지 않은 할일은 null
  final int? issue;

  /// 전환된 업무 요약 정보 (워크스페이스/제목 등)
  final TodoIssueInfo? issueInfo;

  const TodoItem({
    required this.pk,
    required this.user,
    required this.title,
    this.completed = false,
    this.softDeleted = false,
    this.issue,
    this.issueInfo,
  });

  /// 업무로 전환된 할일인지 여부
  bool get isConverted => issue != null;

  factory TodoItem.fromJson(Map<String, dynamic> json) {
    final rawInfo = json['issue_info'];
    return TodoItem(
      pk: json['pk'] as int? ?? 0,
      user: json['user'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      completed: json['completed'] as bool? ?? false,
      softDeleted: json['soft_deleted'] as bool? ?? false,
      issue: json['issue'] as int?,
      issueInfo: rawInfo is Map<String, dynamic>
          ? TodoIssueInfo.fromJson(rawInfo)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'pk': pk,
      'user': user,
      'title': title,
      'completed': completed,
      'soft_deleted': softDeleted,
      'issue': issue,
      'issue_info': issueInfo?.toJson(),
    };
  }

  TodoItem copyWith({
    int? pk,
    int? user,
    String? title,
    bool? completed,
    bool? softDeleted,
    int? issue,
    TodoIssueInfo? issueInfo,
  }) {
    return TodoItem(
      pk: pk ?? this.pk,
      user: user ?? this.user,
      title: title ?? this.title,
      completed: completed ?? this.completed,
      softDeleted: softDeleted ?? this.softDeleted,
      issue: issue ?? this.issue,
      issueInfo: issueInfo ?? this.issueInfo,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TodoItem &&
          runtimeType == other.runtimeType &&
          pk == other.pk &&
          title == other.title &&
          completed == other.completed &&
          softDeleted == other.softDeleted &&
          issue == other.issue &&
          issueInfo == other.issueInfo;

  @override
  int get hashCode =>
      pk.hashCode ^
      title.hashCode ^
      completed.hashCode ^
      softDeleted.hashCode ^
      issue.hashCode ^
      issueInfo.hashCode;
}

/// 할일 → 업무 전환 API(`convert_to_issue`) 응답
@immutable
class TodoConvertResult {
  final TodoItem todo;
  final TodoIssueInfo issue;

  const TodoConvertResult({required this.todo, required this.issue});

  factory TodoConvertResult.fromJson(Map<String, dynamic> json) {
    return TodoConvertResult(
      todo: TodoItem.fromJson(json['todo'] as Map<String, dynamic>),
      issue: TodoIssueInfo.fromJson(json['issue'] as Map<String, dynamic>),
    );
  }
}
