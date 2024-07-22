import Heading from "../ui/Heading.jsx";
import { TbSettingsFilled } from "react-icons/tb";
import { Description } from "../ui/Description.jsx";
import SubmissionsInfo from "../features/codeforces/SubmissionInfo.jsx";
import { redirect, useLoaderData } from "react-router-dom";
import { getContest, getSelectors } from "../api/contests.js";

export async function loader({ params }) {
  if (!localStorage.getItem("api") || !localStorage.getItem("secret")) {
    return redirect("/contests");
  }

  const info = await getContest(
    params.contestId,
    JSON.parse(localStorage.getItem("api")),
    JSON.parse(localStorage.getItem("secret")),
  );
  const selectors = await getSelectors();
  return { info, selectors };
}

function Settings() {
  const { info, selectors } = useLoaderData();
  const groupID = new URLSearchParams(window.location.search).get("group");

  return (
    <>
      <Heading as="h1">
        <TbSettingsFilled />
        Set up the contest
      </Heading>
      <Description>
        <p>
          On this page you can upload the participants&apos; results in .csv
          file
          <br />
          To do this, specify the maximum number of points for each task <br />
        </p>
        <p>You can also copy the list of undefined participants</p>
      </Description>
      <SubmissionsInfo info={info} selectors={selectors} group={groupID} />
    </>
  );
}

export default Settings;
