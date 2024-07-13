import Link from "next/link";
import { DynamicEmbeddedWidget } from "@dynamic-labs/sdk-react-core";
import { FolderIcon, HomeIcon, UsersIcon } from "@heroicons/react/24/outline";
import { Popover, PopoverContent, PopoverTrigger } from "~~/components/UI/Popover";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: HomeIcon, current: true },
  { name: "Admin", href: "/dashboard/admin", icon: UsersIcon, current: false },
  { name: "Projects", href: "/dashboard/projects", icon: FolderIcon, current: false },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-8 bg-slate-950">
      <div className="flex grow col-span-2 flex-col gap-y-5 overflow-y-auto bg-slate-900 px-6">
        <div className="flex h-16 shrink-0 items-center">
          <Link href={"'"}>
            <img
              alt="Your Company"
              src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500"
              className="h-8 w-auto"
            />
          </Link>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map(item => (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className={`group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 ${
                        item.current ? "bg-gray-800 text-white" : "text-gray-400 hover:bg-gray-800 hover:text-white"
                      }`}
                    >
                      {item.icon && <item.icon className="h-6 w-6 shrink-0" aria-hidden="true" />}
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </li>
            <li className="-mx-6 mt-auto">
              <Popover>
                <PopoverContent className="bg-transparent">
                  <div className="w-full bg-white/5 shadow-2xl ring-1 ring-white/10">
                    <DynamicEmbeddedWidget />
                  </div>
                </PopoverContent>
                <PopoverTrigger className="w-full flex justify-end">
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
        <main className="p-6">{children}</main>
      </div>
    </div>
  );
}
