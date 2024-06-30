import styled from "styled-components";
import { useState } from "react";
import toast from "react-hot-toast";
import Heading from "./Heading.jsx";
import Input from "./Input.jsx";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm } from "react-hook-form";
import Button from "./Button.jsx";
import SpinnerMini from "./SpinnnerMini.jsx";

const StyledCover = styled.div`
  position: relative;
  max-width: 90rem;
  gap: 1rem;

  text-align: center;
  color: var(--color-grey-600);
  font-size: 1.6rem;
  font-weight: 500;
  padding: 3rem 4.5rem 5rem;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);
`;

const ButtonBack = styled.button`
  position: absolute;
  left: 2rem;
  top: 2rem;
  background-color: transparent;
  border: none;

  svg {
    width: 3.2rem;
    height: 3.2rem;
    transition: fill 0.3s ease;
  }
  &:hover svg {
    fill: var(--color-brand-600);
  }
`;

const Description = styled.div`
  display: flex;
  justify-content: center;

  &:not(:last-child) {
    margin-bottom: 3.5rem;
  }
`;

const List = styled.form`
  margin: 0 auto;
  max-width: 60rem;
`;
const Item = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  padding-bottom: 2rem;
  column-gap: 0.8rem;

  font-weight: 400;

  &:not(:last-child) {
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--color-grey-200);
  }

  strong {
    font-weight: 500;
  }

  > strong {
    font-size: 2rem;
  }
  > strong:not(:last-child) {
    margin-bottom: 1.5rem;
  }
  > input:not(:last-child) {
    margin-bottom: 0.2rem;
  }
`;

const ItemRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;

  &:last-child {
    margin-top: 2rem;
  }
`;

const ItemInput = styled(Input)`
  max-width: 20rem;
  margin: 0 auto;
  text-align: center;
  padding: 0.3rem 1rem;
  font-size: 1.4rem;

  &:not(:last-child) {
    margin-bottom: 0.5rem;
  }
`;

const Error = styled.span`
  font-size: 1.4rem;
  color: var(--color-red-700);
`;

function SumbissionInfo({ info, reset }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [isGetting, setIsGetting] = useState(false);

  async function handlePostRequest(data) {
    setIsGetting(true);
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
    const response = await fetch("http://10.90.137.106:8000/moodle_grades", {
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

  const onSubmit = function (data) {
    handlePostRequest(data)
      .then((res) => res.blob())
      .then((blob) => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
        setIsGetting(false);
      })
      .catch((err) => {
        toast.error(err.message);
        setIsGetting(false);
      });
  };

  return (
    <StyledCover>
      <ButtonBack onClick={() => reset({})}>
        <BsFillArrowLeftSquareFill />
      </ButtonBack>
      <Heading as="h2">Contest &quot;{info.name}&quot;</Heading>
      <Description>
        Total number of problems: {info.problems.length}
      </Description>
      <List onSubmit={handleSubmit(onSubmit)}>
        {info.problems.map((item, index) => (
          <Item key={index}>
            <strong>
              {item.index} (&quot;{item.name}&quot;)
            </strong>
            <ItemInput
              placeholder="Maximum points per task"
              data-index={index}
              disabled={isGetting}
              {...register(`${index}`, {
                required: "This field is required",
                pattern: {
                  value: /^\d*\.?\d*$/,
                  message: "Incorrect value",
                },
              })}
            />
            {errors[`${index}`] && <Error>{errors[`${index}`].message}</Error>}
            <ItemRow>
              <span>
                Total number of sumbissions:{" "}
                <strong>{item.submissions.length}</strong>
              </span>
              <span>
                Undefined participants: <strong>X</strong>
              </span>
            </ItemRow>
          </Item>
        ))}
        <Button disabled={isGetting}>
          {isGetting ? <SpinnerMini /> : "Create a rating file"}
        </Button>
      </List>
    </StyledCover>
  );
}

export default SumbissionInfo;
