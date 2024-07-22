import toast from "react-hot-toast";

export async function getContest(contestID, APIKey, secretKey) {
  const url = `/api/contests/${contestID}?key=${APIKey}&secret=${secretKey}`;

  const response = await fetch(url);

  if (!response.ok) {
    const data = await response.json();
    console.log("Contest could not be loaded: ", data);

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

export async function getGrouped(json, file) {
  console.log(json, file);
  const formData = new FormData();
  formData.append("submissions_archive", file);
  formData.append("results_data", JSON.stringify(json));

  const url = "/api/moodle-grades/with-archive";
  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw response;
  }

  return response;
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

  let attemptsResponse;
  if (data["attempts"].length) {
    attemptsResponse = await getGrouped(body, data["attempts"][0]);
  }

  console.log("Server answer for grouping: ", attemptsResponse);
  if (attemptsResponse && !attemptsResponse.ok) {
    toast.error(
      "Something went wrong with mapping attempts: ",
      attemptsResponse?.statusText,
    );
  }

  const gradesResponse = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(body),
  });

  console.log("Server answer for file generating", gradesResponse);

  if (!gradesResponse.ok) {
    throw new Error(gradesResponse.statusText);
  }
  return [attemptsResponse, gradesResponse];
}
