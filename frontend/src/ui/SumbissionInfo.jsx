import styled from "styled-components";
import { useState } from "react";
import toast from "react-hot-toast";
import Heading from "./Heading.jsx";
import Input from "./Input.jsx";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import { useForm } from "react-hook-form";
import Button from "./Button.jsx";
import SpinnerMini from "./SpinnnerMini.jsx";
import { useMoveBack } from "../hooks/useMoveBack.js";

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
    width: 5rem;
    height: 5rem;
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

  span {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
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

function SumbissionsInfo({ info }) {
  const moveBack = useMoveBack();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [isGetting, setIsGetting] = useState(false);

  const onSubmit = function (data) {
    setIsGetting(true);

    handlePostRequest(data)
      .then((res) => res.blob())
      .then((blob) => {
        var file = window.URL.createObjectURL(blob);
        window.location.assign(file);
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
      <ButtonBack onClick={moveBack}>
        <BsFillArrowLeftSquareFill />
      </ButtonBack>
      <Heading as="h2">Contest &quot;{info.name}&quot;</Heading>
      <Description>
        Total number of problems: {info.problems.length}
      </Description>
      <List onSubmit={handleSubmit(onSubmit)}>
        {info.problems.map((item, index) => (
          <SubmissionItem key={index} item={item}>
            <>
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
              {errors[`${index}`] && (
                <Error>{errors[`${index}`].message}</Error>
              )}
            </>
          </SubmissionItem>
        ))}
        <Button disabled={isGetting}>
          {isGetting ? <SpinnerMini /> : "Create a rating file"}
        </Button>
      </List>
    </StyledCover>
  );
}

function SubmissionItem({ index, item, children }) {
  const undefinedUsers = item.submissions.filter((item) => !item.author.email);
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Item key={index}>
      {children}
      <ItemRow>
        <span>
          Total number of sumbissions:
          <strong>{item?.submissions?.length}</strong>
        </span>

        {undefinedUsers.length > 0 ? (
          <span>
            Undefined participants: <strong>{undefinedUsers?.length}</strong>
            <Button size="small">{!isOpen ? "SHOW" : "HIDE"}</Button>
          </span>
        ) : (
          <span>All users are defined</span>
        )}
      </ItemRow>
    </Item>
  );
}

export default SumbissionsInfo;
