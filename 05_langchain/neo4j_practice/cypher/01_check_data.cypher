// NODE 이름과 노드별 수 확인
MATCH (node)
RETURN
    labels(node) as labels,
    count(node) as count
ORDER BY labels;

// 학생 ID가 중복되는 Student Node 검색
MATCH (student:Student)
WITH 
    student.student_id as student_id,
    count(*) as count
WHERE count > 1
RETURN student_id, count;

// 강의 ID가 중복되는 Course Node 검색
MATCH (course:Course)
WITH 
    course.course_id as course_id,
    count(*) as count
WHERE count > 1
RETURN course_id, count;

// 강사 ID가 중복되는 Instructor Node 검색
MATCH (instructor:Instructor)
WITH 
    instructor.instructor_id as instructor_id,
    count(*) as count
WHERE count > 1
RETURN instructor_id, count;