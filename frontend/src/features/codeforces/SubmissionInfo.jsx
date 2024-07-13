import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm } from "react-hook-form";
import { handlePostRequest } from "../../api/contests.js";
import { useLocalStorageState } from "../../hooks/useLocalStorage.js";
import { Link, useNavigate } from "react-router-dom";
import {
  StyledCover,
  ButtonBack,
  Description,
  List,
  Item,
  ItemRow,
  ItemInput,
  Error,
  UndefinedUsersList,
  UndefinedDescription,
} from "./SubmissionsInfo.components.jsx";
import Button from "../../ui/Button.jsx";
import Heading from "../../ui/Heading.jsx";
import SpinnerMini from "../../ui/SpinnerMini.jsx";

function SubmissionsInfo({ info }) {
  const definedUsers = {
    ...info,
    problems: info.problems.map((item) => {
      return {
        ...item,
        submissions: item.submissions.filter(
          (item) => item.author.email != null,
        ),
      };
    }),
  };
  const unpossibleReqest = definedUsers.problems.every(
    (item) => item.submissions.length === 0,
  );

  const navigate = useNavigate();

  const [contestPoints, setContestPoints] = useLocalStorageState(
    [],
    `contest-${info.id}`,
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm();

  useEffect(() => {
    const subscription = watch((value) => {
      setContestPoints(
        Object.values(value).map((item) => parseFloat(item) || undefined),
      );
    });
    return () => subscription.unsubscribe();
  }, [setContestPoints, watch]);

  const [isGetting, setIsGetting] = useState(false);

  const onSubmit = function (data) {
    setIsGetting(true);

    handlePostRequest(definedUsers, data)
      .then((res) => {
        return res.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `FileName.pdf`);

        // Append to html link element page
        document.body.appendChild(link);

        // Start download
        link.click();

        // Clean up and remove the link
        link.parentNode.removeChild(link);
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => {
        setIsGetting(false);
      });
  };

  return (
    <StyledCover>
      <ButtonBack onClick={() => navigate("/submissions")}>
        <BsFillArrowLeftSquareFill />
      </ButtonBack>
      <Heading as="h2">Contest &quot;{info.name}&quot;</Heading>
      <Description>
        Total number of problems: {info.problems.length}
      </Description>
      <List onSubmit={handleSubmit(onSubmit)}>
        {info.problems.map((item, index) => (
          <SubmissionItem key={index} item={item} index={index}>
            <>
              <strong>
                {item.index} (&quot;{item.name}&quot;)
              </strong>
              <ItemInput
                placeholder="Maximum points per task"
                data-index={index}
                disabled={isGetting}
                defaultValue={contestPoints[index]}
                {...register(`${index}`, {
                  required: "This field is required",
                  pattern: {
                    value: /^\d*\.?\d*$/,
                    message: "Incorrect value",
                  },
                })}
              />
              {errors[`${index}`] && (
                <Error>{errors[`${index}`].message}</Error>
              )}
            </>
          </SubmissionItem>
        ))}
        {unpossibleReqest ? (
          <UndefinedDescription style={{ fontWeight: "400" }}>
            There are no solutions that could be obtained, please{" "}
            <b>wait for the end of the contest</b> or{" "}
            <Link to="/handles">download the handles</Link> of the participants
          </UndefinedDescription>
        ) : (
          <Button disabled={isGetting} type="submit">
            {isGetting ? <SpinnerMini /> : "Create a rating file"}
          </Button>
        )}
      </List>
    </StyledCover>
  );
}

function SubmissionItem({ index, item, children }) {
  const undefinedUsers = item.submissions.filter((item) => !item.author.email);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Item undefined={undefinedUsers.length}>
      {children}
      <ItemRow>
        <span>
          Total number of sumbissions:
          <strong>{item?.submissions?.length}</strong>
        </span>

        {undefinedUsers.length > 0 ? (
          <span>
            Undefined participants: <strong>{undefinedUsers?.length}</strong>
            <Button
              size="small"
              type="button"
              onClick={() => setIsOpen((open) => !open)}
            >
              {!isOpen ? "SHOW" : "HIDE"}
            </Button>
          </span>
        ) : (
          <span>All users are defined</span>
        )}
      </ItemRow>
      {isOpen && (
        <UndefinedUsersList id={`list-${index}`}>
          {undefinedUsers.map((user) => (
            <span key={user?.author?.handle}>{user?.author?.handle}</span>
          ))}
        </UndefinedUsersList>
      )}
    </Item>
  );
}
export default SubmissionsInfo;
