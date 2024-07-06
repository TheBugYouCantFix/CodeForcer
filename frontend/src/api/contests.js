// const uri = process.env.REACT_APP_API_URL;

export async function getContest(contestID, APIKey, secretKey) {
  // const url = `https://13bd4039-c465-4f54-b961-30824dc7cc9b.mock.pstmn.io/contests/52`;
  const url = `http://10.90.137.106:8000/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw response;
  }

  const data = response.json();
  return data;
}

export async function handlePostRequest(info, data) {
  const url = "http://10.90.137.106:8000/moodle_grades";
  const body = {
    contest: {
      ...info,
      problems: info.problems.map((item, index) => {
        return {
          ...item,
          max_grade: parseFloat(data[`${index}`]),
          submissions: item.submissions.map((item) => {
            return {
              ...item,
              author_email: item?.author?.email || "",
              points: item?.points || 0,
            };
          }),
        };
      }),
    },
    legally_excused: [],
    late_submission_rules: {},
  };

  console.log("Post request body:", body);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  console.log("Server answer for file generating", response);

  if (response.status >= 500) {
    throw new Error("Something went wrong with CodeForces");
  } else if (!response.ok) {
    throw new Error("Something went wrong!");
  }
  return response;
}
