"use client";

import Link from "next/link";
import { DynamicEmbeddedWidget, useDynamicContext } from "@dynamic-labs/sdk-react-core";
import type { NextPage } from "next";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

const Home: NextPage = () => {
  const { primaryWallet } = useDynamicContext();

  const connectedAddress = primaryWallet?.address;

  return (
    <>
      <div className="relative  dark:bg-dot-white/[0.1] isolate overflow-hidden bg-slate-950">
        {/* <svg
          aria-hidden="true"
          className="absolute inset-0 -z-10 h-full w-full stroke-white/10 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
        >
          <defs>
            <pattern
              x="50%"
              y={-1}
              id="983e3e4c-de6d-4c3f-8d64-b9761d1534cc"
              width={200}
              height={200}
              patternUnits="userSpaceOnUse"
            >
              <path d="M.5 200V.5H200" fill="none" />
            </pattern>
          </defs>
          <svg x="50%" y={-1} className="overflow-visible fill-gray-800/20">
            <path
              d="M-200 0h201v201h-201Z M600 0h201v201h-201Z M-400 600h201v201h-201Z M200 800h201v201h-201Z"
              strokeWidth={0}
            />
          </svg>
          <rect fill="url(#983e3e4c-de6d-4c3f-8d64-b9761d1534cc)" width="100%" height="100%" strokeWidth={0} />
        </svg> */}

        <div
          aria-hidden="true"
          className="absolute left-[calc(50%-4rem)] top-10 -z-10 transform-gpu blur-3xl sm:left-[calc(50%-18rem)] lg:left-48 lg:top-[calc(50%-30rem)] xl:left-[calc(50%-24rem)]"
        >
          <div
            style={{
              clipPath:
                "polygon(73.6% 51.7%, 91.7% 11.8%, 100% 46.4%, 97.4% 82.2%, 92.5% 84.9%, 75.7% 64%, 55.3% 47.5%, 46.5% 49.4%, 45% 62.9%, 50.3% 87.2%, 21.3% 64.1%, 0.1% 100%, 5.4% 51.1%, 21.4% 63.9%, 58.9% 0.2%, 73.6% 51.7%)",
            }}
            className="aspect-[1108/632] w-[69.25rem] bg-gradient-to-r from-[#80caff] to-[#4f46e5] opacity-20"
          />
        </div>
        <div className="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex justify-center lg:px-8 lg:py-40">
          <div className="mx-auto flex flex-col max-w-2xl flex-shrink-0 lg:mx-0 lg:max-w-xl lg:pt-8">
            <div className="mt-24 sm:mt-32 lg:mt-16">
              <a href="#" className="inline-flex space-x-6">
                <span className="rounded-full bg-indigo-/10 px-3 py-1 text-sm font-semibold leading-6 text-[hsl(151,64%,68%)] ring-1 ring-inset ring-[hsl(151,75%,58%)]/20 ">
                  Decentralised Energy Community (DEC)
                </span>
                <span className="inline-flex items-center space-x-2 text-sm font-medium leading-6 text-gray-300">
                  <span>Just shipped v0.0.0.1</span>
                  <ChevronRightIcon aria-hidden="true" className="h-5 w-5 text-gray-500" />
                </span>
              </a>
            </div>
            <h1 className="mt-10 text-4xl font-bold tracking-tight text-white sm:text-6xl">
              Join the <span className="text-[hsl(151,75%,58%)] ">DEC</span> revolution
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-300">
              The community-driven platform for energy sharing and trading. Join the revolution and start earning today.
            </p>
            <div className="mt-10 place-self-start flex items-center justify-center gap-x-6">
              {connectedAddress ? (
                <Link
                  className="p-4 border transition-all hover:bg-[hsl(111,55%,52%)]/20 border-[hsl(111,55%,52%)]/30"
                  href="/dashboard"
                >
                  {" "}
                  Head to Dashboard{" "}
                  <span className="text-[hsl(111,55%,52%)]" aria-hidden="true">
                    →
                  </span>{" "}
                </Link>
              ) : (
                <a href="#" className="text-sm text-white font-semibold leading-6">
                  Get started{" "}
                </a>
              )}
            </div>
          </div>
          <div className=" mt-16 backdrop-blur-sm lg:max-w-96 w-full sm:mt-24 lg:ml-10 ">
            <div className="w-full">
              <div className="w-full   bg-white/5 shadow-2xl ring-1 ring-white/10">
                <DynamicEmbeddedWidget />
              </div>
            </div>
          </div>
        </div>

        {/* <div className="min-h-[100vh] grid grid-cols-8">
          <div className="flex grow col-span-2 flex-col gap-y-5 overflow-y-auto bg-slate-900 px-6">
            <div className="flex h-16 shrink-0 items-center">
              <img
                alt="Your Company"
                src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
                className="h-8 w-auto"
              />
            </div>
            <nav className="flex flex-1 flex-col">
              <ul role="list" className="flex flex-1 flex-col gap-y-7">
                <li>
                  <ul role="list" className="-mx-2 space-y-1">
                    {navigation.map(item => (
                      <li key={item.name}>
                        <a
                          href={item.href}
                          className={cn(
                            item.current
                              ? "bg-gray-800 text-white"
                              : "text-gray-400 hover:bg-gray-800 hover:text-white",
                            "group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6",
                          )}
                        >
                          {item.icon && <item.icon aria-hidden="true" className="h-6 w-6 shrink-0" />}
                          {item.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                </li>

                <li className="-mx-6 mt-auto">
                  <Popover>
                    <PopoverContent className="bg-transparent">
                      <div className="w-full">
                        <div className="w-full   bg-white/5 shadow-2xl ring-1 ring-white/10">
                          <DynamicEmbeddedWidget />
                        </div>
                      </div>
                    </PopoverContent>

                    <PopoverTrigger>
                      <div className="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-white hover:bg-gray-800">
                        <img
                          alt=""
                          src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                          className="h-8 w-8 rounded-full bg-gray-800"
                        />
                        <span className="sr-only">Your profile</span>
                        <span aria-hidden="true">Tim Apple</span>
                      </div>
                    </PopoverTrigger>
                  </Popover>
                </li>
              </ul>
            </nav>
          </div>

          <div className="col-span-6">
            <div className="bg-white/5 shadow-2xl p-6">
              <div className="px-8">
                <h2 className="text-lg font-semibold text-white">Your Hub </h2>
                <div className="grid gap-2 grid-cols-3">
                  <div className="col-span-1">
                    <ChartComponent />
                  </div>
                  <div className="col-span-2">
                    <ChartComponent />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div> */}
      </div>
      {/* <div className="flex items-center flex-col flex-grow pt-10">
        <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-[5rem]">
          <span className="text-[hsl(280,100%,70%)]">DEC</span>
        </h1>
        <div className="px-5">
          <div className="flex justify-center items-center space-x-2 flex-col sm:flex-row">
            <p className="my-2 font-medium">Connected Address:</p>

            <Address address={connectedAddress} />
          </div>
          {primaryWallet && !transactionSignature && (
            <div className="flex justify-center items-center space-x-2 flex-col sm:flex-row">
              <button onClick={() => handleSendTransaction()} className="btn btn-primary">
                Send 0.001 ETH to yourself
              </button>
              <button onClick={() => handleSignMesssage()} className="btn btn-primary">
                Sign Hello World
              </button>
            </div>
          )}
          {primaryWallet && messageSignature && (
            <p className="text-center-text-lg">Message signed! {messageSignature}</p>
          )}
          {primaryWallet && transactionSignature && (
            <p className="text-center-text-lg">Transaction processed! {transactionSignature}</p>
          )}
          <p className="text-center text-lg">
            Get started by editing{" "}
            <code className="italic bg-base-300 text-base font-bold max-w-full break-words break-all inline-block">
              packages/nextjs/app/page.tsx
            </code>
          </p>
          <p className="text-center text-lg">
            Edit your smart contract{" "}
            <code className="italic bg-base-300 text-base font-bold max-w-full break-words break-all inline-block">
              YourContract.sol
            </code>{" "}
            in{" "}
            <code className="italic bg-base-300 text-base font-bold max-w-full break-words break-all inline-block">
              packages/hardhat/contracts
            </code>
          </p>
        </div>

        <div className="flex-grow bg-base-300 w-full mt-16 px-8 py-12">
          <div className="flex justify-center items-center gap-12 flex-col sm:flex-row">
            <div className="flex flex-col bg-base-100 px-10 py-10 text-center items-center max-w-xs rounded-3xl">
              <BugAntIcon className="h-8 w-8 fill-secondary" />
              <p>
                Tinker with your smart contract using the{" "}
                <Link href="/debug" passHref prefetch={false} className="link">
                  Debug Contracts
                </Link>{" "}
                tab.
              </p>
            </div>
            <div className="flex flex-col bg-base-100 px-10 py-10 text-center items-center max-w-xs rounded-3xl">
              <MagnifyingGlassIcon className="h-8 w-8 fill-secondary" />
              <p>
                Explore your local transactions with the{" "}
                <Link href="/blockexplorer" passHref className="link">
                  Block Explorer
                </Link>{" "}
                tab.
              </p>
            </div>
          </div>
        </div>
      </div> */}
    </>
  );
};

export default Home;
