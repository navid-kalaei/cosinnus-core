import React from "react"

import {
  Container,
  Center,
  Box,
  Button,
  Heading
} from '@chakra-ui/react'

import { fetchUser } from "../../store/user"
import { logout } from "../../store/auth"
import { useAppDispatch, RootState } from "../../store"
import { useSelector } from 'react-redux'
import { Redirect } from 'react-router-dom'


export function ProfilePage() {

  const user = useSelector((state: RootState) => state.user);
  const dispatch = useAppDispatch();
  dispatch(fetchUser())


  return (
    <Container maxW='2xl'>
      <Box mt={100} mb={5} px={5} pt={5} pb={100} border='1px' borderColor='gray.200'>
        <Center>
          {user &&
            <Box>
              <Heading>Hello</Heading>
              <Center>
                <Button colorScheme="blue" onClick={() => dispatch(logout())}>LogOut</Button>
              </Center>
            </Box>
          }
        </Center>
      </Box>
    </Container>
  )
}