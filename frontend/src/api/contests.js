export async function getContest(contestID, APIKey, secretKey) {
  const url = `/api/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url);

  if (!response.ok) {
    const data = await response.json();
    console.log(data);

    throw response;
  }

  const data = await response.json();
  return data;
}

export async function getSelectors() {
  const url = `/api/moodle-grades/submission-selectors`;
  const response = await fetch(url);

  if (!response.ok) {
    throw response;
  }

  const data = await response.json();
  return data;
}

export async function getLegal(file) {
  const formData = new FormData();
  formData.append("file", file);
  const url = "/api/moodle-grades/legal-excuses-file";

  const response = await fetch(url, {
    method: "PATCH",
    body: formData,
  });

  if (!response.ok) {
    throw response;
  }

  const data = await response.json();

  return data;
}

export async function handlePostRequest(info, data) {
  let legal_exuses = {};
  if (data["legal-exuses"].length) {
    legal_exuses = await getLegal(data["legal-exuses"][0]);
  }

  const penalty = data.penalty ? parseFloat(data.penalty) / 100 : 0;
  const additionTime =
    parseFloat(data["additional-days"] ? data["additional-days"] : 0) * 86400 +
    parseFloat(data["additional-hours"] ? data["additional-hours"] : 0) * 3600 +
    parseFloat(data["additional-minutes"] ? data["additional-minutes"] : 0) *
      60;

  const url = `/api/moodle-grades`;
  const body = {
    contest: {
      ...info,
      problems: info.problems.map((item) => {
        return {
          ...item,
          submissions: item.submissions.map((item) => {
            return {
              ...item,
              author_email: item.author.email,
            };
          }),
        };
      }),
    },
    problem_max_grade_by_index: info.problems.reduce(
      (acc, cur, idx) => ({
        ...acc,
        [cur.index]: parseFloat(data[idx.toString()]),
      }),
      {},
    ),
    legal_excuses: legal_exuses,
    late_submission_policy: {
      penalty: penalty < 0 ? 0 : penalty > 1 ? 1 : penalty,
      extra_time: additionTime,
    },
    submission_selector_name: data.selector.value,
  };

  console.log("Body of request:", body);

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  console.log("Server answer for file generating", response);

  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return response;
}
