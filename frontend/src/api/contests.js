export async function getContest(contestID, APIKey, secretKey) {
  const url = `https://13bd4039-c465-4f54-b961-30824dc7cc9b.mock.pstmn.io/contests/52`;
  // const url = `http://10.90.137.106:8000/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url, {
    // mode: "no-cors",
  });

  if (!response.ok) {
    throw response;
  }

  const data = response.json();
  return data;
}
export async function handlePostRequest(data) {
  const url = "http://10.90.137.106:8000/moodle_grades";
  const verdicts = {
    1: "FAILED",
    2: "OK",
    3: "PARTIAL",
    4: "COMPILATION_ERROR",
    5: "RUNTIME_ERROR",
    6: "WRONG_ANSWER",
    7: "PRESENTATION_ERROR",
    8: "TIME_LIMIT_EXCEEDED",
    9: "MEMORY_LIMIT_EXCEEDED",
    10: "IDLENESS_LIMIT_EXCEEDED",
    11: "SECURITY_VIOLATED",
    12: "CRASHED",
    13: "INPUT_PREPARATION_CRASHED",
    14: "CHALLENGED",
    15: "SKIPPED",
    16: "TESTING",
    17: "REJECTED",
  };
  const body = {
    contest: {
      id: info.id,
      name: info.name,
      problems: info.problems.map((item, index) => {
        return {
          name: item.name,
          index: item.index,
          max_points: parseFloat(data[`${index}`]),
          max_grade: parseFloat(data[`${index}`]),
          submissions: item.submissions.map((item) => {
            return {
              id: item?.id,
              author_email: item?.author?.email || "",
              verdict: verdicts[item?.verdict],
              passed_test_count: item?.passed_test_count,
              points: item?.points || 0,
              programming_language: item?.programming_language,
            };
          }),
        };
      }),
    },
    plagiarizers: [],
    legally_excused: [],
    late_submission_rules: {},
  };
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });
  if (response.status >= 500) {
    throw new Error("Something went wrong with CodeForces");
  } else if (!response.ok) {
    throw new Error("Something went wrong!");
  }
  return response;
}
